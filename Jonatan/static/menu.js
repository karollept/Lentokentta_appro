
const menuBtn = document.getElementById("menu-btn");
const navMenu = document.getElementById("nav-menu");

menuBtn.addEventListener("click", (e) => {
  menuBtn.classList.toggle("active");
  navMenu.classList.toggle("active");
  e.stopPropagation();
});

document.addEventListener("click", (e) => {
  if (
    navMenu.classList.contains("active") &&
    !navMenu.contains(e.target) &&
    !menuBtn.contains(e.target)
  ) {
    navMenu.classList.remove("active");
    menuBtn.classList.remove("active");
  }
});
