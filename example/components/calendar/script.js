(function () {
  if (document.querySelector(".calendar-component")) {
    document.querySelectorAll(".calendar-component").forEach(elem => elem.onclick = function () {
      alert("Clicked calendar!");
    });
  }
})();
