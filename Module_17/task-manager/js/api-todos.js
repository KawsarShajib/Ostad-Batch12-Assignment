// ===================================================
// Task 3 & 4: API Integration + Dynamic Rendering
// ===================================================

const API_URL = "https://jsonplaceholder.typicode.com/todos";
// documentation = https://jsonplaceholder.typicode.com/?utm_source=chatgpt.com

// DATA
let apiTodos = [];
let currentFilter = "all"; // "all" | "completed" | "pending"

// DOM references
const apiList = document.getElementById("api-list");
const apiMessage = document.getElementById("api-message");
const apiCount = document.getElementById("api-count");
const filterButtons = document.querySelectorAll(".filter-btn");

// ---------- Task 3: fetch data with async/await ----------
async function fetchTodos() {
  apiMessage.className = "message";
  apiMessage.textContent = "Loading todos...";
  apiList.innerHTML = "";

  try {
    const response = await fetch(API_URL);

    // fetch() does not throw on 404/500, so check manually
    if (!response.ok) {
      throw new Error("Server responded with status " + response.status);
    }

    apiTodos = await response.json(); // convert response to JSON
    apiMessage.textContent = ""; // hide loading message
    renderApiTodos();
  } catch (error) {
    apiMessage.className = "message error";
    apiMessage.textContent =
      "Failed to load todos. " + error.message + ". Please check your connection and try again.";
  }
}

// ---------- Task 4: filter + render ----------
function getFilteredTodos() {
  if (currentFilter === "completed") {
    return apiTodos.filter((todo) => todo.completed);
  }
  if (currentFilter === "pending") {
    return apiTodos.filter((todo) => !todo.completed);
  }
  return apiTodos;
}

function renderApiTodos() {
  const list = getFilteredTodos();
  apiList.innerHTML = "";
  apiCount.textContent = "Showing " + list.length + " of " + apiTodos.length + " todos";

  list.forEach((todo) => {
    const li = document.createElement("li");
    li.className = "item" + (todo.completed ? " done" : "");

    const id = document.createElement("span");
    id.className = "id";
    id.textContent = "#" + todo.id;

    const title = document.createElement("span");
    title.className = "title";
    title.textContent = todo.title;

    const status = document.createElement("span");
    status.className = "badge " + (todo.completed ? "badge-done" : "badge-pending");
    status.textContent = todo.completed ? "Completed" : "Pending";

    li.append(id, title, status);
    apiList.appendChild(li);
  });
}

function setFilter(filter) {
  currentFilter = filter;
  filterButtons.forEach((btn) => {
    btn.classList.toggle("active", btn.dataset.filter === filter);
  });
  renderApiTodos();
}

filterButtons.forEach((btn) => {
  btn.addEventListener("click", () => setFilter(btn.dataset.filter));
});

fetchTodos(); // run when page loads
