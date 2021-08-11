M.AutoInit();

document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.sidenav');
    var carousel = document.querySelectorAll('.carousel');
    var elemsSelect = document.querySelectorAll('select');

    var optionsCarousel = {
      padding: 50,
    }

    var instancesSidenav = M.Sidenav.init(elems);
    var instancesCarousel = M.Carousel.init(carousel, optionsCarousel);
    var instancesSelect = M.FormSelect.init(elemsSelect);
  });