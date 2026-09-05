import fs from 'node:fs/promises';
import { Linter } from 'eslint';
import js from '@eslint/js';
import stylelint from 'stylelint';
import { lint } from 'markdownlint/promise';

const [kind, ...files] = process.argv.slice(2);
let failed = false;
if (kind === 'javascript') {
  const linter = new Linter();
  for (const file of files) {
    // QML library pragmas are not ECMAScript; preserve their line positions.
    const text = (await fs.readFile(file, 'utf8')).replace(/^\.pragma library[ \t]*$/gm, '');
    const messages = linter.verify(text, [{
      languageOptions: { ecmaVersion: 'latest', sourceType: file.endsWith('.mjs') || /^\s*(?:import|export)\s/m.test(text) ? 'module' : 'commonjs' },
      rules: { ...js.configs.recommended.rules,
        // Globals and exported entry points depend on Node, browser, or QML hosts.
        // Native type/QML checks own name resolution; this gate checks JS logic.
        'no-undef': 'off', 'no-unused-vars': 'off',
        'no-empty': ['error', { allowEmptyCatch: true }],
        // Control-character rejection and literal whitespace fixtures are intentional.
        'no-control-regex': 'off', 'no-regex-spaces': 'off', 'no-useless-escape': 'off' },
    }]);
    for (const m of messages) console.error(`${file}:${m.line}:${m.column}: ${m.ruleId ?? 'parse'} ${m.message}`);
    failed ||= messages.some(m => m.severity === 2);
  }
} else if (kind === 'css') {
  const result = await stylelint.lint({ files, config: { rules: {
    'block-no-empty': true, 'color-no-invalid-hex': true,
    'declaration-block-no-duplicate-properties': [true, { ignore: ['consecutive-duplicates-with-different-syntaxes'] }],
    'font-family-no-duplicate-names': true, 'function-calc-no-unspaced-operator': true,
    'keyframe-declaration-no-important': true, 'property-no-unknown': true,
    'selector-pseudo-class-no-unknown': true, 'selector-pseudo-element-no-unknown': true,
    'string-no-newline': true, 'unit-no-unknown': true,
  } } });
  for (const r of result.results) for (const m of r.warnings) console.error(`${r.source}:${m.line}:${m.column}: ${m.text}`);
  failed = result.errored;
} else if (kind === 'markdown') {
  const result = await lint({ files, config: { default: false,
    MD011: true, MD018: true, MD019: true, MD020: true, MD021: true,
    MD034: false, MD037: true, MD038: true, MD039: true, MD042: true,
  } });
  for (const [file, messages] of Object.entries(result)) for (const m of messages) console.error(`${file}:${m.lineNumber}: ${m.ruleNames[0]} ${m.ruleDescription}`);
  failed = Object.values(result).some(messages => messages.length);
} else {
  throw new Error(`Unknown lint kind: ${kind}`);
}
process.exitCode = failed ? 1 : 0;
