// ===================================================
// Task 1: Asynchronous JavaScript Practice
// ===================================================



// ---------------------------------------------------
// 1 & 2. EXECUTION CONTEXT + EVENT LOOP
// ---------------------------------------------------
// Execution context: JS runs code inside a "context". The Global
// Execution Context is created first; each function call creates a
// new one that is pushed on the Call Stack and popped when finished.
//
// Event loop: it watches the Call Stack. When the stack is empty it
// moves waiting work into it. Order of priority:
//   1) Synchronous code (call stack)
//   2) Microtasks (Promise .then / await)
//   3) Macrotasks (setTimeout, setInterval)

function runExecutionOrder() {

  console.log("--- 1. Execution Context / 2. Event Loop ---");
  console.log("1. Start (synchronous)");

  setTimeout(() => {
    console.log("4. setTimeout callback (macrotask - runs last)");
  }, 0);

  Promise.resolve().then(() => {
    console.log("3. Promise.then (microtask - runs before setTimeout)");
  });

  console.log("2. End (synchronous)");
}

// ---------------------------------------------------
// 3. setTimeout() - message after 3 seconds
// ---------------------------------------------------
function runTimeout() {
  console.log("\n");
  console.log("--- 3. setTimeout() ---");
  console.log("Waiting 3 seconds...");
  setTimeout(() => {
    console.log("Hello! This message appeared after 3 seconds.");
  }, 3000);
}

// ---------------------------------------------------
// 4. setInterval() - simple countdown timer
// ---------------------------------------------------
let countdownId = null;

function runCountdown() {
  if (countdownId) clearInterval(countdownId); // avoid two timers at once

  let seconds = 5;
  console.log("\n");
  console.log("--- 4. setInterval() ---");
  console.log("Countdown: " + seconds);

  countdownId = setInterval(() => {
    seconds--;
    if (seconds > 0) {
      console.log("Countdown: " + seconds);
    } else {
      console.log("Time's up!");
      clearInterval(countdownId); // always stop an interval
      countdownId = null;
    }
  }, 1000);
}

// ---------------------------------------------------
// 5. CALLBACK FUNCTION
// ---------------------------------------------------
// A callback is a function passed into another function
// to be called later.
function fetchUser(name, callback) {
  console.log("\n");
  console.log("--- 5. Callback Function ---");
  console.log("Fetching user...");
  setTimeout(() => {
    callback(name); // call the function we were given
  }, 1500);
}

function greetUser(name) {
  console.log("Welcome, " + name + "!");
}

function runCallback() {
  fetchUser("Bangladesh !!", greetUser);
}

// ---------------------------------------------------
// 6. PROMISE with resolve AND reject
// ---------------------------------------------------
function checkAge(age) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (age >= 18) {
        resolve("Age " + age + ": Access granted.");
      } else {
        reject("Age " + age + ": Access denied (must be 18+).");
      }
    }, 1000);
  });
}

function runPromise() {
  console.log("\n");
  console.log("--- 6. PROMISE with resolve AND reject ---");
  console.log("Checking ages with Promises (.then/.catch)...");

  checkAge(20)
    .then((result) => console.log("Success: " + result))
    .catch((error) => console.log("Error: " + error));

  checkAge(15)
    .then((result) => console.log("Success: " + result))
    .catch((error) => console.log("Error: " + error));
}

// ---------------------------------------------------
// 7. ASYNC/AWAIT - same example as above, rewritten
// ---------------------------------------------------
async function checkAgeAsync(age) {
  try {
    const result = await checkAge(age); // waits for the Promise
    console.log("\n");
    console.log("--- 7. ASYNC/AWAIT ---");
    console.log("Success: " + result);
  } catch (error) {
    console.log("Error: " + error);
  }
}

async function runAsync() {
  console.log("\n");
  console.log("Checking ages with async/await...");
  await checkAgeAsync(20); // one after the other
  await checkAgeAsync(15);
  console.log("Done.");
}

// ---------------------------------------------------
// Connect buttons
// ---------------------------------------------------
document.getElementById("btn-order").addEventListener("click", runExecutionOrder);
document.getElementById("btn-timeout").addEventListener("click", runTimeout);
document.getElementById("btn-countdown").addEventListener("click", runCountdown);
document.getElementById("btn-callback").addEventListener("click", runCallback);
document.getElementById("btn-promise").addEventListener("click", runPromise);
document.getElementById("btn-async").addEventListener("click", runAsync);
