const typeofObj = typeof {};

const eitherIsNil = (a, b) => a == null || b == null;

export const hashDiff = (a, b) => {
  return eitherIsNil(a, b) || a.hash() !== b.hash();
};

export const shallowObjDiff = (a, b) => {
  if (eitherIsNil(a, b) && !(a == null && b == null)) {
    return true;
  }

  if (a === b) {
    // can't do a diff on the same obj
    return false;
  }

  // non-object values can be compared with the equality operator
  if (typeof a !== typeofObj || typeof b !== typeofObj) {
    return a !== b;
  }

  let aKeys = Object.keys(a);
  let bKeys = Object.keys(b);
  let mismatches = key => a[key] !== b[key];

  if (aKeys.length !== bKeys.length) {
    return true;
  }

  if (aKeys.some(mismatches) || bKeys.some(mismatches)) {
    return true;
  }

  return false;
};
