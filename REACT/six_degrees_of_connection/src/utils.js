// utils.js

/**
 * Filters the results to include only the last repository link for each user.
 * @param {Array} results - The results array from the server response.
 * @returns {Array} - The filtered results array.
 */

const filterResults = (results) => {
  return results.map((item) => {
    if (item[0]) {
      return [[item[0][item[0].length - 1]], item[1]];
    }
    return item;
  });
};

export default filterResults;
