const suggestions = document.getElementById("suggestions");
const searchProduct = document.getElementById("search_product");

// Adding spinner to wait for the data to load
function addSpinner() {
  spinner.classList.add("loader");
}

//Removing spinner
function hideSpinner() {
  spinner.classList.remove("loader");
}

function searchHandler(e) {
  const query = e.target.value;
  search(query);
}

//Getting the list of all DB products and fetching the ones matching user's input
async function search(str) {
  clearSuggestions();
  if (!str) return;

  const wordLower = str.toLowerCase();
  addSpinner();
  const resp = await axios.get("/api/products");

  const products = [];
  for (let product of resp.data) {
    products.push(product);
  }
  hideSpinner();
  const results = products.filter((product) => {
    const productLower = product["product_name"].toLowerCase();
    return productLower.includes(wordLower);
  });

  showSuggestions(results);
}

function clearSuggestions() {
  const currentLi = suggestions.querySelectorAll("li");
  currentLi.forEach((li) => li.remove());
}
//function to display all the results in the dropdow
function showSuggestions(results) {
  results
    .map((result) =>
      createLiSuggestion(
        result["product_name"],
        result["id"],
        result["category_id"],
        result["category_name"]
      )
    )
    .forEach((li) => suggestions.append(li));
}

//create new elements - li to display all of the suggestions
function createLiSuggestion(
  productName,
  productId,
  productCategoryId,
  productCategoryName
) {
  const newLi = document.createElement("li");
  newLi.innerText = `${productName} - ${productCategoryName} `;
  newLi.dataset.productId = productId;
  newLi.dataset.categoryId = productCategoryId;
  newLi.classList.add("dropdown-item");
  return newLi;
}

//once the user selects one of the suggestion, the selected only will be populated in the bar
function useSuggestion(e) {
  e.preventDefault();
  const selectedProductName = e.target.innerText;
  searchProduct.value = selectedProductName;
  searchProduct.dataset.productId = e.target.dataset.productId;

  clearSuggestions();
}

export {
  addSpinner,
  hideSpinner,
  searchHandler,
  search,
  showSuggestions,
  createLiSuggestion,
  clearSuggestions,
  useSuggestion,
};
