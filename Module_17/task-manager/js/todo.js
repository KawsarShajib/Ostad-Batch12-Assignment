// ===================================================
// Task 2: Todo / Task Manager App
// Pattern: data array -> update functions -> render()
// ===================================================

// 1. DATA: the single source of truth
let todos = [];
let nextId = 1;

// 2. DOM references (selected once)
const todoForm = document.getElementById("todo-form");
const todoInput = document.getElementById("todo-input");
const todoError = document.getElementById("todo-error");
const todoList = document.getElementById("todo-list");
const statTotal = document.getElementById("stat-total");
const statCompleted = document.getElementById("stat-completed");
const statPending = document.getElementById("stat-pending");

// 3. DATA FUNCTIONS (they only change the array, then call render)
function addTask(title) {
  todos.push({ id: nextId++, title: title, completed: false });
  renderTodos();
}

function toggleTask(id) {
  todos = todos.map((todo) =>
    todo.id === id ? { ...todo, completed: !todo.completed } : todo
  );
  renderTodos();
}

function deleteTask(id) {
  todos = todos.filter((todo) => todo.id !== id);
  renderTodos();
}

// 4. RENDER FUNCTION: rebuilds the UI from the array
function renderTodos() {
  todoList.innerHTML = "";

  if (todos.length === 0) {
    const empty = document.createElement("li");
    empty.className = "empty";
    empty.textContent = "No tasks yet. Add one above!";
    todoList.appendChild(empty);
  }

  todos.forEach((todo) => {
    const li = document.createElement("li");
    li.className = "item" + (todo.completed ? " done" : "");

    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.checked = todo.completed;
    checkbox.dataset.action = "toggle";
    checkbox.dataset.id = todo.id;

    const text = document.createElement("span");
    text.className = "title";
    text.textContent = todo.title; // textContent is safe from HTML injection

    const delBtn = document.createElement("button");
    delBtn.className = "danger";
    delBtn.textContent = "Delete";
    delBtn.dataset.action = "delete";
    delBtn.dataset.id = todo.id;

    li.append(checkbox, text, delBtn);
    todoList.appendChild(li);
  });

  updateStats();
}

function updateStats() {
  const completed = todos.filter((todo) => todo.completed).length;
  statTotal.textContent = todos.length;
  statCompleted.textContent = completed;
  statPending.textContent = todos.length - completed;
}

// 5. EVENTS
todoForm.addEventListener("submit", (event) => {
  event.preventDefault(); // stop page reload
  const title = todoInput.value.trim();

  if (title === "") {
    todoError.textContent = "Please enter a task.";
    return;
  }

  todoError.textContent = "";
  addTask(title);
  todoInput.value = "";
  todoInput.focus();
});

// Event delegation: one listener handles every checkbox/delete button
todoList.addEventListener("click", (event) => {
  const { action, id } = event.target.dataset;
  if (!action) return;

  if (action === "toggle") toggleTask(Number(id));
  if (action === "delete") deleteTask(Number(id));
});

renderTodos(); // first draw
