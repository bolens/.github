"""Exercise the exact shared workflow script against GitHub API fixtures."""
import json
from pathlib import Path
import subprocess
import textwrap
import unittest

WORKFLOW = Path(__file__).resolve().parents[1] / '.github/workflows/reusable-auto-assign.yml'
SCRIPT = textwrap.dedent(WORKFLOW.read_text().split('          script: |\n', 1)[1])
HARNESS = r'''
const fixture = JSON.parse(process.argv[1]);
const calls = [];
const item = fixture.item || {number: 7, state: 'open', assignees: []};
const context = {
  repo: {owner: fixture.owner || 'bolens', repo: 'example'},
  eventName: fixture.event || 'issues',
  issue: {number: fixture.number === undefined ? 7 : fixture.number},
  payload: {sender: {login: fixture.author || 'someone-else'}},
};
const api = {
  get: async args => {
    calls.push(['get', args]);
    if (fixture.readError) throw Error('read failed');
    return {data: item};
  },
  listForRepo: () => {},
  addAssignees: async args => {
    calls.push(['add', args]);
    if (fixture.writeError) throw Error('write failed');
    return {data: {assignees: fixture.ignoreAssignment ? [] : [{login: 'bolens'}]}};
  },
};
const github = {
  rest: {issues: api},
  paginate: async (method, args) => {
    if (method !== api.listForRepo) throw Error('wrong pagination endpoint');
    calls.push(['paginate', args]);
    return fixture.items || [item];
  },
};
const AsyncFunction = Object.getPrototypeOf(async function(){}).constructor;
(async () => {
  let error = null;
  try { await new AsyncFunction('github', 'context', 'core', fixture.script)(
    github, context, {info: () => {}},
  ); } catch (e) { error = e.message; }
  process.stdout.write(JSON.stringify({calls, error}));
})();
'''


class MaintainerAssignment(unittest.TestCase):
    def run_workflow(self, **fixture):
        fixture['script'] = SCRIPT
        result = subprocess.run(['node', '-e', HARNESS, json.dumps(fixture)],
                                check=True, capture_output=True, text=True)
        return json.loads(result.stdout)

    def test_issue_and_pr_authors_do_not_change_the_assignee(self):
        for event in ['issues', 'pull_request_target']:
            for author in ['bolens', 'dependabot[bot]', 'external-contributor']:
                with self.subTest(event=event, author=author):
                    result = self.run_workflow(event=event, author=author)
                    self.assertIsNone(result['error'])
                    self.assertEqual(['get', 'add'], [c[0] for c in result['calls']])
                    self.assertEqual(['bolens'], result['calls'][1][1]['assignees'])

    def test_current_state_prevents_closed_or_duplicate_writes(self):
        for item in [dict(number=7, state='closed', assignees=[]),
                     dict(number=7, state='open', assignees=[{'login': 'Bolens'}])]:
            result = self.run_workflow(item=item)
            self.assertIsNone(result['error'])
            self.assertEqual(['get'], [c[0] for c in result['calls']])

    def test_coassignees_are_preserved_by_additive_assignment(self):
        result = self.run_workflow(item=dict(number=7, state='open',
                                            assignees=[{'login': 'collaborator'}]))
        self.assertIsNone(result['error'])
        self.assertEqual(['bolens'], result['calls'][1][1]['assignees'])

    def test_manual_and_scheduled_reconciliation_use_pagination(self):
        for event in ['schedule', 'workflow_dispatch']:
            items = [dict(number=n, state='open', assignees=[]) for n in range(1, 205)]
            items.append(dict(number=205, state='open', assignees=[{'login': 'bolens'}]))
            result = self.run_workflow(event=event, items=items)
            self.assertIsNone(result['error'])
            self.assertEqual('paginate', result['calls'][0][0])
            self.assertEqual('open', result['calls'][0][1]['state'])
            self.assertEqual(100, result['calls'][0][1]['per_page'])
            self.assertEqual(204, len(result['calls']) - 1)

    def test_empty_reconciliation_is_a_noop(self):
        result = self.run_workflow(event='schedule', items=[])
        self.assertIsNone(result['error'])
        self.assertEqual(['paginate'], [c[0] for c in result['calls']])

    def test_invalid_event_owner_or_item_never_reaches_the_api(self):
        for fixture in [dict(owner='another-owner'), dict(event='push'),
                        dict(number=0), dict(number='7'), dict(number=1.5)]:
            result = self.run_workflow(**fixture)
            self.assertIsNotNone(result['error'])
            self.assertEqual([], result['calls'])

    def test_api_errors_are_not_silenced(self):
        for fixture in [dict(readError=True), dict(writeError=True),
                        dict(ignoreAssignment=True)]:
            result = self.run_workflow(**fixture)
            self.assertIsNotNone(result['error'])
