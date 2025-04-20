let sideBar = document.querySelector(".side-bar");

document.querySelector("#menu-btn").onclick = () => {
  sideBar.classList.toggle("active");
};

document.querySelector("#close-side-bar").onclick = () => {
  sideBar.classList.remove("active");
};

let searchForm = document.querySelector(".search-form");

document.querySelector("#search-btn").onclick = () => {
  searchForm.classList.toggle("active");
};

window.onscroll = () => {
  sideBar.classList.remove("active");
  searchForm.classList.remove("active");
};
var swiper = new Swiper(".home-slider", {
  loop: true,
  grabCursor: true,
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
});

const mobileBrands = ["Samsung", "Apple", "Vivo", "Realme", "Xiaomi", "OnePlus", "Motorola"];
const laptopBrands = ["Dell", "HP", "Lenovo", "Asus", "Acer", "MSI", "Apple", "Samsung"];

function populateBrands(brands) {
  const brand1 = document.getElementById("brand1");
  const brand2 = document.getElementById("brand2");
  brand1.innerHTML = '<option value="">Select Brand</option>';
  brand2.innerHTML = '<option value="">Select Brand</option>';
  brands.forEach(brand => {
    brand1.innerHTML += `<option value="${brand}">${brand}</option>`;
    brand2.innerHTML += `<option value="${brand}">${brand}</option>`;
  });
}

function onCategoryChange(value) {
  const brandSection = document.getElementById("brandDropdowns");
  const keywordInput = document.getElementById("clothesKeyword");
  if (value === "Mobiles") {
    brandSection.style.display = "flex";
    keywordInput.style.display = "none";
    populateBrands(mobileBrands);
  } else if (value === "Laptops") {
    brandSection.style.display = "flex";
    keywordInput.style.display = "none";
    populateBrands(laptopBrands);
  } else if (value === "Clothes") {
    brandSection.style.display = "none";
    keywordInput.style.display = "inline-block";
  } else {
    brandSection.style.display = "none";
    keywordInput.style.display = "none";
  }
}
function toggleCompareButton() {
  const checkboxes = document.querySelectorAll("input[name='selected_products']:checked");
  const compareBtn = document.getElementById('compareBtn');
  if (checkboxes.length >= 2) {
    compareBtn.style.display = 'inline-block';
  } else {
    compareBtn.style.display = 'none';
  }
}

document.addEventListener('DOMContentLoaded', function () {
  const checkboxes = document.querySelectorAll("input[name='selected_products']");
  checkboxes.forEach(checkbox => {
    checkbox.addEventListener('change', toggleCompareButton);
  });
});