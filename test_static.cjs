const assert = require('node:assert/strict');
const fs = require('node:fs');
const predict = require('./inference.js');
const model = JSON.parse(fs.readFileSync('model.json','utf8'));
const fixtures = JSON.parse(fs.readFileSync('synthetic_checks.json','utf8'));
for (const f of fixtures) {
  const r = predict(model, f.input);
  assert.ok(Math.abs(r.probability-f.expected_probability)<1e-5, 'Python/JS prediction mismatch');
  assert.equal(r.prediction, Number(f.expected_probability>=.5));
}
const base = fixtures[0].input;
assert.equal(predict(model,{...base,EDUCATION:0}).probability,predict(model,{...base,EDUCATION:5}).probability);
for(const change of [{AGE:NaN},{SEX:9},{PAY_AMT1:-1},{LIMIT_BAL:''}])
  assert.throws(()=>predict(model,{...base,...change}));
assert.match(fs.readFileSync('README.md','utf8'),/^sdk: static$/m);
console.log('Static inference tests passed.');
