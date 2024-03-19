import {
  addSpinner,
  hideSpinner,
  searchHandler,
  search,
  showSuggestions,
  createLiSuggestion,
  clearSuggestions,
  useSuggestion,
} from "./modules/products_suggestions.js";

// Getting DOM elements for reminders page
const searchProduct = document.getElementById("search_product");
const quantityReminder = document.getElementById("quantity_reminder");
const btnAddReminder = document.getElementById("btn-add-reminder");
const reminderListProducts = document.getElementById("reminder-products");
const suggestions = document.getElementById("suggestions");
const btnSaveEdit = document.getElementById("save-edit");
const editedQuantity = document.getElementById("quantity_reminder_edit");
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

//Adding new reminder to don't forget list
async function newReminder(e) {
  const product_id = searchProduct.dataset.productId;
  const quantity = quantityReminder.value;
  const resp = await axios.post("/api/reminders/products", {
    product_id: product_id,
    quantity: quantity,
  });
  if (resp.status === 201) {
    const msg = "Product has been added to your don't forget list";
    showErrors(msg);
  }

  searchProduct.value = "";
  quantityReminder.value = "";
  loadMyReminders();
}

// Getting user's reminders
async function loadMyReminders() {
  addSpinner();
  const resp = await axios.get("/api/reminders/products");
  const products = resp.data["data"];
  hideSpinner();
  removeProductsFromPage();
  addProductsToPage(products);
}

function removeProductsFromPage() {
  const currentProducts = reminderListProducts.querySelectorAll("li");
  currentProducts.forEach((li) => li.remove());
}

// Loading user's reminders details (all products)
function addProductsToPage(products) {
  products.forEach((product) => {
    let li = document.createElement("li");
    li.innerText = `${product["product_name"]}, Quantity: `;
    li.classList.add("list-group-item");
    li.classList.add("text-bg-secondary");
    li.dataset.reminderId = product["id"];

    let spanQty = document.createElement("input");
    spanQty.type = "number";
    spanQty.min = "1";
    spanQty.value = product["quantity"];
    spanQty.name = "quantity_reminder_edit";
    spanQty.id = "quantity_reminder_edit";
    li.append(spanQty);

    let span = document.createElement("span");
    span.innerText = product["category_name"];
    span.classList.add("badge");
    span.classList.add("text-bg-light");
    li.append(span);

    let delButton = document.createElement("button");
    delButton.innerText = "Delete";
    delButton.id = "btnDelItem";
    delButton.classList.add("btn");
    delButton.classList.add("btn-danger");
    delButton.classList.add("btn-sm");
    li.append(delButton);

    let editButton = document.createElement("button");
    editButton.innerText = "Save";
    editButton.id = "btnSaveItem";
    editButton.classList.add("btn");
    editButton.classList.add("btn-success");
    editButton.classList.add("btn-sm");
    li.append(editButton);

    reminderListProducts.append(li);
  });
}
//Handling delete option of single item
async function deleteReminderProduct(e) {
  const item = e.target.parentElement;
  const itemId = item.dataset.reminderId;

  addSpinner();
  const resp = await axios.delete(`/api/reminders/products/${itemId}`);
  if (resp.status === 200) {
    const msg = "Product has been deleted from your list";
    showErrors(msg);
  }
  hideSpinner();
  loadMyReminders();
}

//Saving the updated quantity of a single reminder item
async function saveEditReminder(e) {
  const id = e.target.parentElement.dataset.reminderId;
  const quantity = e.target.parentElement.children[0].value;
  const resp = await axios.patch("/api/remiders/products", {
    id: id,
    quantity: quantity,
  });
  if (resp.status === 201) {
    const msg = "Product has been updated";
    showErrors(msg);
  }

  loadMyReminders();
}

//As starting point - loading all user's reminders
hidePageComponents();
loadMyReminders();

searchProduct.addEventListener("keyup", searchHandler);

suggestions.addEventListener("click", useSuggestion);

btnAddReminder.addEventListener("shown.bs.modal", function (e) {
  e.preventDefault();
});

reminderListProducts.addEventListener("click", function (e) {
  e.preventDefault();
  if (e.target.id === "btnDelItem") {
    deleteReminderProduct(e);
  }
});

reminderListProducts.addEventListener("click", function (e) {
  e.preventDefault();
  if (e.target.id === "btnSaveItem") {
    saveEditReminder(e);
  }
});

btnSaveEdit.addEventListener("click", function (e) {
  e.preventDefault();
  newReminder(e);
});
