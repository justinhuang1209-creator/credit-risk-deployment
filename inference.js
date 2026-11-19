(function(root) {
  'use strict';
  function predict(model, record) {
    const values = {};
    for (const key of model.features) {
      if (record[key] === '' || record[key] === null || record[key] === undefined || !Number.isFinite(Number(record[key])))
        throw new Error('Enter a finite number for ' + key);
      values[key] = Number(record[key]);
    }
    for (const key of model.categorical.columns) {
      const v = values[key];
      const allowed = key === 'SEX' ? [1,2] : key === 'EDUCATION' ? [0,1,2,3,4,5,6] : key === 'MARRIAGE' ? [0,1,2,3] : [-2,-1,0,1,2,3,4,5,6,7,8];
      if (!allowed.includes(v)) throw new Error('Invalid category for ' + key);
    }
    if (values.AGE < 18 || values.AGE > 120 || !Number.isInteger(values.AGE)) throw new Error('Age must be a whole number from 18 to 120.');
    if (values.LIMIT_BAL <= 0) throw new Error('Credit limit must be positive.');
    for (const key of model.features.filter(k => k.startsWith('PAY_AMT')))
      if (values[key] < 0) throw new Error('Payment amounts cannot be negative.');
    if ([5,6].includes(values.EDUCATION)) values.EDUCATION = 0;
    let x = model.numeric.columns.map((key,i) => Math.fround((values[key]-model.numeric.mean[i])/model.numeric.scale[i]));
    model.categorical.columns.forEach((key,i) => {
      for (const category of model.categorical.categories[i]) x.push(values[key] === category ? 1 : 0);
    });
    for (const layer of model.layers) {
      x = layer.bias.map((bias,j) => {
        let sum = bias;
        for (let i=0;i<x.length;i++) sum += x[i]*layer.weights[i][j];
        return layer.activation === 'relu' ? Math.max(0,sum) : 1/(1+Math.exp(-sum));
      });
    }
    return {probability:x[0], prediction:Number(x[0]>=model.threshold)};
  }
  root.creditPredict = predict;
  if (typeof module !== 'undefined') module.exports = predict;
})(typeof globalThis !== 'undefined' ? globalThis : this);
