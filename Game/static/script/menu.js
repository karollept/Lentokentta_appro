const menuButton = document.getElementById("menu-btn");
const navigationMenu = document.getElementById("nav-menu");

menuButton.addEventListener("click", (event) => {
  menuButton.classList.toggle("active");
  navigationMenu.classList.toggle("active");
  event.stopPropagation();
});

document.addEventListener("click", (event) => {
  const menuIsOpen = navigationMenu.classList.contains("active");
  const clickedInsideMenu = navigationMenu.contains(event.target);
  const clickedMenuButton = menuButton.contains(event.target);

  if (menuIsOpen && !clickedInsideMenu && !clickedMenuButton) {
    navigationMenu.classList.remove("active");
    menuButton.classList.remove("active");
  }
});

const logoutButton = document.getElementById("logout-btn");

logoutButton.addEventListener("click", async () => {
  try {
    await safeFetch(`${currentAPI}/logout`, { method: "POST" });
  } catch (err) {
    console.warn("Logout request failed or timed out:", err);
  }

  try {
    localStorage.removeItem("auth_token");
    sessionStorage.clear();
  } catch (_) {
  }

  window.location.href = "../templates/login.html";
});
