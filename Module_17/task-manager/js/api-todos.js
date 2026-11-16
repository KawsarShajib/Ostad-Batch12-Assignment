// ===================================================
// Task 3 & 4: API Integration + Dynamic Rendering
// ===================================================

const API_URL = "https://jsonplaceholder.typicode.com/todos";
// documentation = https://jsonplaceholder.typicode.com/?utm_source=chatgpt.com

// DATA
let apiTodos = [];
let currentFilter = "all"; // "all" | "completed" | "pending"

let searchTerm = ""; // bonus part (1-search feature)

// DOM references
const apiList = document.getElementById("api-list");
const apiMessage = document.getElementById("api-message");
const apiCount = document.getElementById("api-count");
const filterButtons = document.querySelectorAll(".filter-btn");

const refreshBtn = document.getElementById("refresh-btn"); // bonus part (3-refresh button)
const searchInput = document.getElementById("search-input"); // bonus part (1-search feature)

// ---------- Task 3: fetch data with async/await ----------
async function fetchTodos() {
  apiMessage.className = "message";
  apiMessage.textContent = "Loading todos...";
  apiList.innerHTML = "";

  // bonus part (3-refresh button)
  refreshBtn.disabled = true;               
  refreshBtn.textContent = "Refreshing..."; 

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
  } finally {
    // bonus part (3-refresh button): runs after try OR catch
    refreshBtn.disabled = false;
    refreshBtn.textContent = "🔄 Refresh";
  }
}

// ---------- Task 4: filter + render ----------

// function getFilteredTodos() {
//   if (currentFilter === "completed") {
//     return apiTodos.filter((todo) => todo.completed);
//   }
//   if (currentFilter === "pending") {
//     return apiTodos.filter((todo) => !todo.completed);
//   }
//   return apiTodos;
// }

// ---------- Task 4: filter + render (modified for bonus part (1-search feature) -----------
function getFilteredTodos() {
  let list = apiTodos;

  // 1. Filter by status
  if (currentFilter === "completed") {
    list = list.filter((todo) => todo.completed);
  } else if (currentFilter === "pending") {
    list = list.filter((todo) => !todo.completed);
  }

  // 2. NEW: filter by search text (case-insensitive)
  if (searchTerm !== "") {
    list = list.filter((todo) =>
      todo.title.toLowerCase().includes(searchTerm)
    );
  }

  return list;
}





function renderApiTodos() {
  const list = getFilteredTodos();
  apiList.innerHTML = "";
  apiCount.textContent = "Showing " + list.length + " of " + apiTodos.length + " todos";

// bonus part (1-search feature)
  if (list.length === 0) {
      const empty = document.createElement("li");
      empty.className = "empty";
      empty.textContent = "No todos found.";
      apiList.appendChild(empty);
      return;
  }
// bonus part (1-search feature)

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

// bonus part (1-search feature)
searchInput.addEventListener("input", () => {
  searchTerm = searchInput.value.trim().toLowerCase();
  renderApiTodos();
});

refreshBtn.addEventListener("click", fetchTodos); // bonus part (3-refresh button)

fetchTodos(); // run when page loads
