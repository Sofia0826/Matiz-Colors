// document.addEventListener("DOMContentLoaded", function () {
//     const track = document.querySelector(".carousel-track");
//     const slides = document.querySelectorAll(".slide");
//     const prevButton = document.querySelector(".prev");
//     const nextButton = document.querySelector(".next");
    
//     let index = 0;
  
//     function updateCarousel() {
//       track.style.transform = `translateX(-${index * 100}%)`;
//     }
  
//     nextButton.addEventListener("click", function () {
//       index = (index + 1) % slides.length;
//       updateCarousel();
//     });
  
//     prevButton.addEventListener("click", function () {
//       index = (index - 1 + slides.length) % slides.length;
//       updateCarousel();
//     });
//   });
  