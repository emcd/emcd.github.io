/* Adapted from:
    - https://css-tricks.com/a-complete-guide-to-dark-mode-on-the-web/#aa-combining-all-the-things
    - https://github.com/pradyunsg/furo/blob/main/src/furo/assets/scripts/furo.js
 */
const btn = document.querySelector(".palette-selector");
const prefersDarkScheme = window.matchMedia("(prefers-color-scheme: dark)").matches;

function setTheme(theme) {
  if (theme == "auto") {
    var trueTheme = prefersDarkScheme ? "dark" : "light";
  } else {
    var trueTheme = theme;
  }
  if (trueTheme == "dark") {
    if (document.body.classList.contains("solarized-light")) {
      document.body.classList.replace("solarized-light", "solarized-dark");
    } else {
      document.body.classList.add("solarized-dark");
    }
  } else if (trueTheme == "light") {
    if (document.body.classList.contains("solarized-dark")) {
      document.body.classList.replace("solarized-dark", "solarized-light");
    } else {
      document.body.classList.add("solarized-light");
    }
  }
  document.body.dataset.theme = theme;
  localStorage.setItem("theme", theme);
}

const initialTheme = localStorage.getItem("theme") || "auto";
setTheme(initialTheme);

btn.addEventListener("click", function () {
  var theme = localStorage.getItem("theme");
  if (prefersDarkScheme) {
    if (theme == "auto") {
      var newTheme = "light";
    } else if (theme == "light") {
      var newTheme = "dark";
    } else {
      var newTheme = "auto";
    }
  } else {
    if (theme == "auto") {
      var newTheme = "dark";
    } else if (theme == "dark") {
      var newTheme = "light";
    } else {
      var newTheme = "auto";
    }
  }
  setTheme(newTheme);
});
