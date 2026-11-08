/*  1. No JavaScript is needed  */
/*  2. No JavaScript is needed  */


/*  3. Dashboard  */
const totalIncomeElement = document.getElementById("totalIncome");
const totalExpensesElement = document.getElementById("totalExpenses");
const currentBalanceElement = document.getElementById("currentBalance");

let transactions = [];

function updateDashboard() {
  let totalIncome = 0;
  let totalExpenses = 0;

  for (let i = 0; i < transactions.length; i++) {
    if (transactions[i].type === "income") {
      totalIncome += transactions[i].amount;
    } else {
      totalExpenses += transactions[i].amount;
    }
  }

  const currentBalance = totalIncome - totalExpenses;

  totalIncomeElement.textContent = totalIncome.toFixed(2);
  totalExpensesElement.textContent = totalExpenses.toFixed(2);
  currentBalanceElement.textContent = currentBalance.toFixed(2);
}


/*  4. Add Transaction  */

const transactionForm = document.getElementById("transactionForm");
const titleInput = document.getElementById("title");
const amountInput = document.getElementById("amount");
const typeInput = document.getElementById("type");
const categoryInput = document.getElementById("category");
const dateInput = document.getElementById("date");

const formMessage = document.getElementById("formMessage");

function showMessage(message, messageType) {
  formMessage.textContent = message;
  formMessage.classList.remove("hidden");

  if (messageType === "success") {
    formMessage.classList.add("success-message");
    formMessage.classList.remove("error-message");
  } else {
    formMessage.classList.add("error-message");
    formMessage.classList.remove("success-message");
  }
}

function addTransaction(event) {
  event.preventDefault();

  const title = titleInput.value.trim();
  const amount = Number(amountInput.value);
  const type = typeInput.value;
  const category = categoryInput.value;
  const date = dateInput.value;

  if (title === "") {
    showMessage("Please enter a transaction title.", "error");
    return;
  }

  if (amount <= 0 || isNaN(amount)) {
    showMessage("Please enter a valid amount greater than 0.", "error");
    return;
  }

  if (type === "") {
    showMessage("Please select a transaction type.", "error");
    return;
  }

  if (category === "") {
    showMessage("Please select a category.", "error");
    return;
  }

  if (date === "") {
    showMessage("Please select a date.", "error");
    return;
  }

  const newTransaction = {
    id: Date.now(),
    title: title,
    amount: amount,
    type: type,
    category: category,
    date: date
  };

  transactions.push(newTransaction);

  transactionForm.reset();
  renderTransactions();
  showMessage("Transaction added successfully!", "success");
}

transactionForm.addEventListener("submit", addTransaction);


/*  5. Transaction History */

const transactionTableBody = document.getElementById("transactionTableBody");
const emptyMessage = document.getElementById("emptyMessage");

function renderTransactions() {
  transactionTableBody.innerHTML = "";

  if (transactions.length === 0) {
    emptyMessage.classList.remove("hidden");
  } else {
    emptyMessage.classList.add("hidden");
  }

  transactions.forEach(function (transaction) {
    const tableRow = document.createElement("tr");

    const amountClass =
      transaction.type === "income" ? "income-text" : "expense-text";

    const titleCell = document.createElement("td");
    titleCell.textContent = transaction.title;

    const amountCell = document.createElement("td");
    amountCell.className = amountClass;
    amountCell.textContent =
      (transaction.type === "income" ? "+" : "-") +
      transaction.amount.toFixed(2);

    const categoryCell = document.createElement("td");
    categoryCell.textContent = transaction.category;

    const typeCell = document.createElement("td");
    typeCell.textContent = transaction.type;

    const dateCell = document.createElement("td");
    dateCell.textContent = transaction.date;

    const actionCell = document.createElement("td");

    const deleteButton = document.createElement("button");
    deleteButton.textContent = "Delete";
    deleteButton.className = "action-button delete-button";

    deleteButton.addEventListener("click", function () {
      deleteTransaction(transaction.id);
    });

    actionCell.appendChild(deleteButton);

    tableRow.appendChild(titleCell);
    tableRow.appendChild(amountCell);
    tableRow.appendChild(categoryCell);
    tableRow.appendChild(typeCell);
    tableRow.appendChild(dateCell);
    tableRow.appendChild(actionCell);

    transactionTableBody.appendChild(tableRow);
  });

  updateDashboard();
}