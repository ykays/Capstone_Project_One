// Getting DOM elements for templates page
const createNewTemplate = document.getElementById("create-template");
const viewTemplate = document.getElementById("view-template");
const btnCreate = document.getElementById("btn-create");
const myTemplateName = document.getElementById("my-template-name-view");
const btnDelete = document.getElementById("btn-delete-template");
const btnEdit = document.getElementById("btn-edit-template");
const messages = document.getElementById("messages");
const editTemplate = document.getElementById("edit-template");
const templateProducts = document.getElementById("template-products");
const myTemplateNameEdit = document.getElementById("my-template-name-edit");
const searchProduct = document.getElementById("search_product");
const suggestions = document.getElementById("suggestions");
const btnAddProduct = document.getElementById("btn-add-product");
const spinner = document.getElementById("spinner");
// Function to hide all page elements until we know if the user has any templates
function hidePageComponents() {
  const components = [createNewTemplate, viewTemplate, editTemplate];
  components.forEach((c) => (c.style.display = "none"));
}

// Adding spinner to wait for the data to load
function addSpinner() {
  spinner.classList.add("loader");
}

//Removing spinner
function hideSpinner() {
  spinner.classList.remove("loader");
}

// Getting user's templates
async function getUsersTemplates() {
  resp = await axios.get("/api/templates");
  if (resp.data.length === 0) {
    hideSpinner();
    createNewTemplate.style.display = "block";
  } else {
    hideSpinner();
    const templateId = resp.data[0]["id"];
    const templateName = resp.data[0]["template_name"];
    const userId = resp.data[0]["user_id"];
    viewMyTemplate(templateId, templateName, userId);
  }
}

// Create new template name
async function createTemplate(e) {
  const name = document.getElementById("template_name").value;
  addSpinner();
  resp = await axios.post("/api/templates", {
    name: name,
  });
  hideSpinner();
  const templateId = resp.data.template["id"];
  const templateName = resp.data.template["template_name"];
  const userId = resp.data.template["user_id"];

  hidePageComponents();
  viewMyTemplate(templateId, templateName, userId);
}

//View user's template to delete it or edit it
function viewMyTemplate(templateId, templateName, userId) {
  viewTemplate.style.display = "block";
  myTemplateName.innerText = templateName;
  btnDelete.dataset.templateId = templateId;
  btnDelete.dataset.userId = userId;
  btnEdit.dataset.templateId = templateId;
  btnEdit.dataset.userId = userId;
}

// Deleting the user's template
async function deleteMyTemplate(e) {
  addSpinner();
  const templateId = e.target.dataset.templateId;
  resp = await axios.delete(`/api/templates/${templateId}`);
  hideSpinner();
  hidePageComponents();
  getUsersTemplates();
}

//Loading user's template
async function loadMyTemplate(id) {
  hidePageComponents();
  editTemplate.style.display = "block";
  addSpinner();
  resp = await axios.get(`/api/templates/${id}`);
  const products = resp.data["data"];
  hideSpinner();
  removeProductsFromPage();
  addProductsToPage(products);
}

function removeProductsFromPage() {
  const currentProducts = templateProducts.querySelectorAll("li");
  currentProducts.forEach((li) => li.remove());
}

// Loading user's template details (all template products)
function addProductsToPage(products) {
  products.forEach((product) => {
    let li = document.createElement("li");
    li.innerText = `${product["product_name"]} `;
    li.classList.add("list-group-item");
    li.classList.add("text-bg-secondary");
    li.dataset.productId = product["id"];

    let span = document.createElement("span");
    span.innerText = product["category_name"];
    span.classList.add("badge");
    span.classList.add("text-bg-light");
    li.append(span);

    let delButton = document.createElement("button");
    delButton.innerText = "X";
    delButton.classList.add("btn");
    delButton.classList.add("btn-danger");
    delButton.classList.add("btn-sm");
    li.append(delButton);

    templateProducts.append(li);
  });
}

//Deleting user's template product and reloading the page with remaning ones
async function deleteTemplateProduct(e) {
  const item = e.target.parentElement;
  const itemId = item.dataset.productId;
  addSpinner();
  resp = await axios.delete(`/api/templates/product/${itemId}`);
  hideSpinner();
  loadMyTemplate(resp.data["template"]);
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
  resp = await axios.get("/api/products");

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
      createLi(
        result["product_name"],
        result["id"],
        result["category_id"],
        result["category_name"]
      )
    )
    .forEach((li) => suggestions.append(li));
}

//create new elements - li to display all of the suggestions
function createLi(
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

//once the user hits Add button the selected suggestion will be added to the user's template
async function addTemplateProduct(e) {
  const itemId = searchProduct.dataset.productId;
  resp = await axios.post(`/api/templates/product/${itemId}`);

  searchProduct.value = "";
  loadMyTemplate(resp.data["template"]);
}

hidePageComponents();
getUsersTemplates();
addSpinner();

btnCreate.addEventListener("click", function (e) {
  e.preventDefault();
  createTemplate(e);
});

btnDelete.addEventListener("click", function (e) {
  e.preventDefault();
  deleteMyTemplate(e);
});

btnEdit.addEventListener("click", function (e) {
  e.preventDefault();
  const templateId = e.target.dataset.templateId;
  loadMyTemplate(templateId);
});

templateProducts.addEventListener("click", function (e) {
  e.preventDefault();
  deleteTemplateProduct(e);
});

searchProduct.addEventListener("keyup", searchHandler);
suggestions.addEventListener("click", useSuggestion);

btnAddProduct.addEventListener("click", function (e) {
  e.preventDefault();
  addTemplateProduct(e);
});
