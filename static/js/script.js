M.AutoInit();

document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.sidenav');
    var carousel = document.querySelectorAll('.carousel');
    var optionsCarousel = {
      padding: 50,
    }
    var instancesSidenav = M.Sidenav.init(elems);
    var instancesCarousel = M.Carousel.init(carousel, optionsCarousel);
  });