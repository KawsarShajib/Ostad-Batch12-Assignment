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

// Create a new transaction
function addTransaction(event) {
  event.preventDefault();

  const title = titleInput.value.trim();
  const amount = Number(amountInput.value);
  const type = typeInput.value;
  const category = categoryInput.value;
  const date = dateInput.value;

  
  // 9. Add form validation---start
  const isValid = validateTransaction(title, amount, type, category, date);

  if (!isValid) {
    return;
  }
  // 9. Add form validation---end



  const newTransaction = {
    id: Date.now(),
    title: title,
    amount: amount,
    type: type,
    category: category,
    date: date
  };

  transactions.push(newTransaction);

  saveTransactions();
  renderTransactions();

  transactionForm.reset();
  showMessage("Transaction added successfully!", "success");
}

/* 
event.preventDefault() stops the browser from reloading the page when the form is submitted. The required attribute provides basic HTML validation, while the JavaScript checks provide clearer custom messages.
*/




/*  5. Transaction History */

const transactionTableBody = document.getElementById("transactionTableBody");
const emptyMessage = document.getElementById("emptyMessage");

// function renderTransactions() {
//   transactionTableBody.innerHTML = "";

//   if (transactions.length === 0) {
//     emptyMessage.classList.remove("hidden");
//   } else {
//     emptyMessage.classList.add("hidden");
//   }

//   transactions.forEach(function (transaction) {
//     const tableRow = document.createElement("tr");

//     const amountClass =
//       transaction.type === "income" ? "income-text" : "expense-text";

//     const titleCell = document.createElement("td");
//     titleCell.textContent = transaction.title;

//     const amountCell = document.createElement("td");
//     amountCell.className = amountClass;
//     amountCell.textContent =
//       (transaction.type === "income" ? "+" : "-") +
//       transaction.amount.toFixed(2);

//     const categoryCell = document.createElement("td");
//     categoryCell.textContent = transaction.category;

//     const typeCell = document.createElement("td");
//     typeCell.textContent = transaction.type;

//     const dateCell = document.createElement("td");
//     dateCell.textContent = transaction.date;

//     const actionCell = document.createElement("td");

//     const deleteButton = document.createElement("button");
//     deleteButton.textContent = "Delete";
//     deleteButton.className = "action-button delete-button";

//     deleteButton.addEventListener("click", function () {
//       deleteTransaction(transaction.id);
//     });

//     actionCell.appendChild(deleteButton);

//     tableRow.appendChild(titleCell);
//     tableRow.appendChild(amountCell);
//     tableRow.appendChild(categoryCell);
//     tableRow.appendChild(typeCell);
//     tableRow.appendChild(dateCell);
//     tableRow.appendChild(actionCell);

//     transactionTableBody.appendChild(tableRow);
//   });

//   updateDashboard();
// }

/* 
Using textContent is safer than innerHTML for user-entered values because it inserts plain text rather than interpreting it as HTML 
*/




/*  7. Updating the renderTransactions Function */

const searchInput = document.getElementById("searchInput");
const filterType = document.getElementById("filterType");

function renderTransactions() {
  transactionTableBody.innerHTML = "";

  const searchText = searchInput.value.toLowerCase();
  const selectedType = filterType.value;

  const filteredTransactions = transactions.filter(function (transaction) {
    const matchesSearch = transaction.title
      .toLowerCase()
      .includes(searchText);

    const matchesType =
      selectedType === "all" || transaction.type === selectedType;

    return matchesSearch && matchesType;
  });

  if (filteredTransactions.length === 0) {
    emptyMessage.classList.remove("hidden");
  } else {
    emptyMessage.classList.add("hidden");
  }

  filteredTransactions.forEach(function (transaction) {
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

    const editButton = document.createElement("button");
    editButton.textContent = "Edit";
    editButton.className = "action-button edit-button";

    const deleteButton = document.createElement("button");
    deleteButton.textContent = "Delete";
    deleteButton.className = "action-button delete-button";

    editButton.addEventListener("click", function () {
      editTransaction(transaction.id);
    });

    deleteButton.addEventListener("click", function () {
      deleteTransaction(transaction.id);
    });

    actionCell.appendChild(editButton);
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
  updateMonthlySummary();
}




searchInput.addEventListener("input", renderTransactions);
filterType.addEventListener("change", renderTransactions);






/*  6. Add delete transaction */

function deleteTransaction(id) {
  const isConfirmed = confirm(
    "Are you sure you want to delete this transaction?"
  );

  if (isConfirmed) {
    transactions = transactions.filter(function (transaction) {
      return transaction.id !== id;
    });

    if (editingId === id) {
      cancelEdit();
    }

    saveTransactions();
    renderTransactions();
  }
}

/* 
The filter() method creates a new array containing every transaction except the one whose id matches the deleted transaction.
*/



/*  8. Add data persistence */

// Save transactions whenever they change, and load them when the page opens.

function saveTransactions() {
  localStorage.setItem("transactions", JSON.stringify(transactions));
}

function loadTransactions() {
  const savedTransactions = localStorage.getItem("transactions");

  if (savedTransactions !== null) {
    transactions = JSON.parse(savedTransactions);
  }

  renderTransactions();
}


/* 
JSON.stringify() turns the JavaScript array into a string for storage; JSON.parse() turns the saved string back into a usable JavaScript array.
*/


/*  9. Add form validation */

function validateTransaction(title, amount, type, category, date) {
  if (title === "") {
    showMessage("Please enter a transaction title.", "error");
    return false;
  }

  if (isNaN(amount) || amount <= 0) {
    showMessage("Please enter a valid amount greater than 0.", "error");
    return false;
  }

  if (type === "") {
    showMessage("Please select a transaction type.", "error");
    return false;
  }

  if (category === "") {
    showMessage("Please select a category.", "error");
    return false;
  }

  if (date === "") {
    showMessage("Please select a date.", "error");
    return false;
  }

  return true;
}



/* 10. Add Edit Transaction */

let editingId = null;

const formTitle = document.getElementById("formTitle");
const submitButton = document.getElementById("submitButton");
const cancelEditButton = document.getElementById("cancelEditButton");

function editTransaction(id) {
  let selectedTransaction = null;

  for (let i = 0; i < transactions.length; i++) {
    if (transactions[i].id === id) {
      selectedTransaction = transactions[i];
    }
  }

  if (selectedTransaction === null) {
    return;
  }

  editingId = id;

  titleInput.value = selectedTransaction.title;
  amountInput.value = selectedTransaction.amount;
  typeInput.value = selectedTransaction.type;
  categoryInput.value = selectedTransaction.category;
  dateInput.value = selectedTransaction.date;

  formTitle.textContent = "Edit Transaction";
  submitButton.textContent = "Update Transaction";
  cancelEditButton.classList.remove("hidden");

  showMessage("Editing transaction. Update the fields and save.", "success");
}

function updateTransaction(event) {
  event.preventDefault();

  const title = titleInput.value.trim();
  const amount = Number(amountInput.value);
  const type = typeInput.value;
  const category = categoryInput.value;
  const date = dateInput.value;

  const isValid = validateTransaction(title, amount, type, category, date);

  if (!isValid) {
    return;
  }

  for (let i = 0; i < transactions.length; i++) {
    if (transactions[i].id === editingId) {
      transactions[i].title = title;
      transactions[i].amount = amount;
      transactions[i].type = type;
      transactions[i].category = category;
      transactions[i].date = date;
    }
  }

  saveTransactions();
  renderTransactions();
  cancelEdit();

  showMessage("Transaction updated successfully!", "success");
}

function cancelEdit() {
  editingId = null;
  transactionForm.reset();

  formTitle.textContent = "Add Transaction";
  submitButton.textContent = "Add Transaction";
  cancelEditButton.classList.add("hidden");
}

transactionForm.addEventListener("submit", function (event) {
  if (editingId === null) {
    addTransaction(event);
  } else {
    updateTransaction(event);
  }
});

cancelEditButton.addEventListener("click", cancelEdit);




/* 11. Monthly Expenses Summary */

const monthlySummary = document.getElementById("monthlySummary");

function updateMonthlySummary() {
  monthlySummary.innerHTML = "";

  const monthlyExpenses = {};

  transactions.forEach(function (transaction) {
    if (transaction.type === "expense") {
      const month = transaction.date.slice(0, 7);

      if (monthlyExpenses[month] === undefined) {
        monthlyExpenses[month] = 0;
      }

      monthlyExpenses[month] += transaction.amount;
    }
  });

  const months = Object.keys(monthlyExpenses);

  if (months.length === 0) {
    const noData = document.createElement("p");
    noData.textContent = "No expense data available yet.";
    monthlySummary.appendChild(noData);
    return;
  }

  months.forEach(function (month) {
    const summaryItem = document.createElement("div");
    summaryItem.className = "monthly-item";

    summaryItem.textContent =
      month + ": " + monthlyExpenses[month].toFixed(2) + " spent";

    monthlySummary.appendChild(summaryItem);
  });
}

// Load saved transactions when the page starts
loadTransactions();



/*

Final JavaScript order : 
========================
01. Get all HTML elements.
02. Create the transactions array and editingId variable.
03. Create saveTransactions() and loadTransactions().
04. Create showMessage() and validateTransaction().
05. Create addTransaction(), editTransaction(), updateTransaction(), and cancelEdit().
06. Create deleteTransaction().
07. Create renderTransactions().
08. Create updateDashboard() and updateMonthlySummary().
09. Add event listeners.
10. Call loadTransactions() at the end.

How the app flows : 
===================
01. The page loads and loadTransactions() reads saved data from localStorage.
02. renderTransactions() displays the saved transactions.
03. updateDashboard() calculates income, expenses, and balance.
04. The user submits the form.
05. JavaScript validates the input.
06. A new transaction object is added to the array.
07. saveTransactions() saves the updated array.
08. renderTransactions() refreshes the table, dashboard, and monthly summary.
09. The user can search, filter, edit, or delete any transaction.
10 Every change updates the display and saves again.

*/