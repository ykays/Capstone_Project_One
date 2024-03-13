// Getting DOM elements for external search page
const searchExt = document.getElementById("search_product_ext");
const btnSearchExt = document.getElementById("btn-add-product-ext");
const suggestionsExt = document.getElementById("suggestions-ext");
const productCategories = document.getElementById("ext_prod_cat");
const btnAddProduct = document.getElementById("btn-add-product-to-products");

//Gettting list of all product categories so they can be displayed as select option
async function getCategories() {
  resp = await axios.get("/categories");
  const results = resp.data;
  results.forEach((result) => createSelectOption(result));
}

function createSelectOption(result) {
  const option = document.createElement("option");
  option.innerText = `${result.id}: ${result.category_name} - ${result.category_details}`;
  option.dataset.categoryId = result.id;
  productCategories.append(option);
}

//Triggering an API to get products from the external source
async function searchExternalAPI() {
  const name = searchExt.value;
  resp = await axios.get(`/search/external/${name}`);

  handlingExternalSearch(resp.data.hints);
}

//Displaying the returned option from the API
function handlingExternalSearch(data) {
  data.forEach((item) => {
    const newLi = document.createElement("li");
    newLi.innerText = `${item.food.label} - ${item.food.category}`;
    newLi.dataset.label = item.food.label;
    newLi.classList.add("dropdown-item");
    suggestionsExt.append(newLi);
  });
}

//Clearing options once user selected one
function clearSuggestions() {
  const currentLi = suggestionsExt.querySelectorAll("li");
  currentLi.forEach((li) => li.remove());
}

//Populate the text input with the selected option
function useSuggestion(e) {
  e.preventDefault();
  const selectedProductName = e.target.dataset.label;
  searchExt.value = selectedProductName;

  clearSuggestions();
}

//Adding product to DB
async function addToProductList(e) {
  const product = searchExt.value;
  const indx = productCategories.value.indexOf(":");
  const category_id = productCategories.value.slice(0, indx);
  resp = await axios.post("/api/products", {
    product: product,
    category_id: category_id,
  });
  searchExt.value = "";
  return resp.data;
}

getCategories();

btnSearchExt.addEventListener("click", function (e) {
  e.preventDefault();
  searchExternalAPI();
});

suggestionsExt.addEventListener("click", useSuggestion);

btnAddProduct.addEventListener("click", function (e) {
  e.preventDefault();
  addToProductList(e);
});
