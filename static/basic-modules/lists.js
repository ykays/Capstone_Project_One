import {
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
} from "./modules/products_suggestions.js";

// Getting DOM elements for grocery list page

const btnDateSubmit = document.getElementById("date-submit");
const formGroceryDate = document.getElementById("grocery-date");
const messages = document.getElementById("messages");

const btnAddToList = document.getElementById("btn-add-to-list");
const btnAddReminders = document.getElementById("btn-add-reminders");
const btnSaveAdd = document.getElementById("save-add");

const searchProduct = document.getElementById("search_product");
const quantityAdd = document.getElementById("quantity_add");
const suggestions = document.getElementById("suggestions");
const listProducts = document.getElementById("list-products");

const priceSection = document.getElementById("price-section");
const priceInput = document.getElementById("price-input");
const btnPriceSubmit = document.getElementById("price-submit");

// Function to hide sections of the pages
function hidePageComponents() {
  const components = [messages, btnAddToList, btnAddReminders, priceSection];
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

async function getList(e) {
  removeProductsFromPage();
  btnAddToList.style.display = "none";
  btnAddReminders.style.display = "none";
  priceSection.style.display = "none";
  const date = formGroceryDate.value;
  addSpinner();
  const resp = await axios.get(`/api/list/products/${date}`);

  hideSpinner();
  if (resp.status === 201) {
    const msg = "A new list has been created";
    showErrors(msg);
  }

  if (resp.status === 200 && resp.data["message"] == "Template needed") {
    const msg = "Please add a template first";
    showErrors(msg);
  } else {
    const resultProducts = resp.data.list;
    btnAddToList.style.display = "block";
    btnAddReminders.style.display = "block";
    priceSection.style.display = "block";
    addProductsToPage(resultProducts);
    priceInput.value = resp.data.list[0].total_price;
  }
}

async function newListProduct(e) {
  const product_id = searchProduct.dataset.productId;
  const quantity = quantityAdd.value;
  const date = formGroceryDate.value;
  const resp = await axios.post("/api/list/products", {
    product_id: product_id,
    quantity: quantity,
    date: date,
  });
  if (resp.status === 201) {
    const msg = "A new product has been added";
    showErrors(msg);
  }
  searchProduct.value = "";
  quantityAdd.value = "";
  getList();
}

//Handling delete option of single item
async function deleteProduct(e) {
  const item = e.target.parentElement;
  const itemId = item.dataset.reminderId;

  addSpinner();
  const resp = await axios.delete(`/api/list/products/${itemId}`);
  hideSpinner();
  if (resp.status === 200) {
    const msg = "A product has been deleted";
    showErrors(msg);
  }
  getList();
}

//Saving the updated quantity of a single reminder item
async function saveEditProduct(e) {
  const id = e.target.parentElement.dataset.reminderId;
  const quantity = e.target.parentElement.children[0].value;
  addSpinner();
  const resp = await axios.patch(`/api/list/products/${id}`, {
    quantity: quantity,
  });
  hideSpinner();
  if (resp.status === 201) {
    const msg = "A product has been updated";
    showErrors(msg);
  }

  getList();
}

async function addRemindersToList(e) {
  const date = formGroceryDate.value;
  addSpinner();
  const resp = await axios.post("/api/list/products/reminders", {
    date: date,
  });
  hideSpinner();
  if (resp.status === 201) {
    const msg = "The products have been added";
    showErrors(msg);
  } else if (resp.status === 200) {
    const msg = "No reminders have been found";
    showErrors(msg);
  }
  getList();
}

async function submitPrice(e) {
  const price = priceInput.value;
  const date = formGroceryDate.value;
  const resp = await axios.patch("/api/list", {
    date: date,
    price: price,
  });
  if (resp.status === 200) {
    const msg = "The price has been updated";
    showErrors(msg);
  }
}

async function markAsChecked(e) {
  const btn = e.target;
  const product = e.target.parentElement;
  const id = product.dataset.reminderId;
  let bought = false;
  if (product.dataset.bought === "false") {
    btn.innerText = "✔";
    product.dataset.bought = true;
    bought = true;
  } else {
    btn.innerText = "□";
    product.dataset.bought = false;
    bought = false;
  }
  const resp = await axios.patch(`/api/list/products/${id}`, {
    bought: bought,
  });
}

hidePageComponents();

searchProduct.addEventListener("keyup", searchHandler);
suggestions.addEventListener("click", useSuggestion);

btnDateSubmit.addEventListener("click", function (e) {
  e.preventDefault();
  getList(e);
});

btnAddToList.addEventListener("shown.bs.modal", function (e) {
  e.preventDefault();
});

btnSaveAdd.addEventListener("click", function (e) {
  e.preventDefault();
  newListProduct(e);
});

listProducts.addEventListener("click", function (e) {
  e.preventDefault();
  if (e.target.id === "btnDelItem") {
    deleteProduct(e);
  }
});

listProducts.addEventListener("click", function (e) {
  e.preventDefault();
  if (e.target.id === "btnSaveItem") {
    saveEditProduct(e);
  }
});

btnAddReminders.addEventListener("click", function (e) {
  e.preventDefault();
  addRemindersToList(e);
});

btnPriceSubmit.addEventListener("click", function (e) {
  e.preventDefault();
  submitPrice(e);
});

listProducts.addEventListener("click", function (e) {
  e.preventDefault();
  if (e.target.id === "btnCheckItem") {
    console.log(e);
    markAsChecked(e);
  }
});
