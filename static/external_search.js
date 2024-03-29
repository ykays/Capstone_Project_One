// Getting DOM elements for external search page
const searchExt = document.getElementById("search_product_ext");
const btnSearchExt = document.getElementById("btn-add-product-ext");
const suggestionsExt = document.getElementById("suggestions-ext");
const productCategories = document.getElementById("ext_prod_cat");
const btnAddProduct = document.getElementById("btn-add-product-to-products");
const messages = document.getElementById("messages");

// Function to hide sections of the pages
function hidePageComponents() {
  const components = [messages];
  components.forEach((c) => (c.style.display = "none"));
}

function showErrors(msg) {
  messages.style.display = "block";
  messages.innerText = msg;
  timeOut();
}
function timeOut() {
  setTimeout(() => {
    messages.innerText = "";
    messages.style.display = "none";
  }, 4000);
}

//Gettting list of all product categories so they can be displayed as select options
async function getCategories() {
  resp = await axios.get("/api/categories");
  const results = resp.data;
  results.forEach((result) => createSelectOption(result));
}

//Creating option element for each of the categories
function createSelectOption(result) {
  const option = document.createElement("option");
  option.innerText = `${result.id}: ${result.category_name} - ${result.category_details}`;
  option.dataset.categoryId = result.id;
  productCategories.append(option);
}

//Triggering an API to get products from the external source
async function searchExternalAPI() {
  const name = searchExt.value;
  if (name === undefined || name === "") {
    const msg = "Please select product";
    showErrors(msg);
    return;
  }
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
  if (product === undefined || product === "") {
    const msg = "Please select product";
    showErrors(msg);
    return;
  }
  const indx = productCategories.value.indexOf(":");
  const category_id = productCategories.value.slice(0, indx);
  if (category_id === "Select Product Categor") {
    const msg = "Please select category";
    showErrors(msg);
    return;
  }

  resp = await axios.post("/api/products", {
    product: product,
    category_id: category_id,
  });
  searchExt.value = "";
  if (resp.status === 200 && resp.data["message"] == "access unauthorized") {
    const msg = "Access unauthorized ";
    showErrors(msg);
  }
  if (resp.status === 200 && resp.data["message"] == "already exists") {
    const msg = "This product & category already exists ";
    showErrors(msg);
  }
  if (resp.status === 201) {
    const msg = "The product has been added to Database ";
    showErrors(msg);
  }
  return resp.data;
}

hidePageComponents();
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
