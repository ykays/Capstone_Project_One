const suggestions = document.getElementById("suggestions");
const searchProduct = document.getElementById("search_product");
const listProducts = document.getElementById("list-products");

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

  const products = resp.data.map((product) => product);

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

function addProductsToPage(products) {
  products.forEach((product) => {
    const li = helperCreateLi(product);

    const spanQty = helperCreateSpanQty(product);
    li.append(spanQty);

    const span = helperCreateSpan(product);
    li.append(span);

    const btnCheck = helperCreateButtonCheck(product);
    li.append(btnCheck);

    const delButton = helperCreateButtonDelete(product);
    li.append(delButton);

    const editButton = helperCreateButtonEdit(product);
    li.append(editButton);

    listProducts.append(li);
  });
}

function helperCreateLi(product) {
  const li = document.createElement("li");
  li.innerText = `${product["product_name"]}, Quantity: `;
  li.classList.add("list-group-item");
  li.classList.add("text-bg-secondary");
  li.dataset.reminderId = product["id"];
  li.dataset.bought = product["bought"];
  return li;
}

function helperCreateButtonCheck(product) {
  const btnCheck = document.createElement("button");
  btnCheck.classList.add("check-btn");
  btnCheck.id = "btnCheckItem";
  product["bought"] === true
    ? (btnCheck.innerText = "✔")
    : (btnCheck.innerText = "□");
  return btnCheck;
}

function helperCreateButtonEdit(product) {
  const editButton = document.createElement("button");
  editButton.innerText = "Save";
  editButton.id = "btnSaveItem";
  editButton.classList.add("btn");
  editButton.classList.add("btn-success");
  editButton.classList.add("btn-sm");
  return editButton;
}

function helperCreateButtonDelete(product) {
  const delButton = document.createElement("button");
  delButton.innerText = "Delete";
  delButton.id = "btnDelItem";
  delButton.classList.add("btn");
  delButton.classList.add("btn-danger");
  delButton.classList.add("btn-sm");
  return delButton;
}

function helperCreateSpanQty(product) {
  const spanQty = document.createElement("input");
  spanQty.type = "number";
  spanQty.min = "1";
  spanQty.value = product["quantity"];
  spanQty.name = "quantity_reminder_edit";
  spanQty.id = "quantity_reminder_edit";
  return spanQty;
}

function helperCreateSpan(product) {
  const span = document.createElement("span");
  span.innerText = product["category_name"];
  span.classList.add("badge");
  span.classList.add("text-bg-light");
  return span;
}

function removeProductsFromPage() {
  const currentProducts = listProducts.querySelectorAll("li");
  currentProducts.forEach((li) => li.remove());
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
  addProductsToPage,
  removeProductsFromPage,
};
