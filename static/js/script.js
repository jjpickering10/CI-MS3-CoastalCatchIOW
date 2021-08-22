// Materialize JS initialisation

M.AutoInit();

document.addEventListener('DOMContentLoaded', function () {
  var elems = document.querySelectorAll('.sidenav');
  var carousel = document.querySelectorAll('.carousel');
  var elemsSelect = document.querySelectorAll('select');
  var elemsCollapse = document.querySelectorAll('.collapsible');
  var elemsModal = document.querySelectorAll('.modal');

  var optionsCarousel = {
    padding: 50,
  }

  var instancesSidenav = M.Sidenav.init(elems);
  var instancesCarousel = M.Carousel.init(carousel, optionsCarousel);
  var instancesSelect = M.FormSelect.init(elemsSelect);
  var instancesCollapse = M.Collapsible.init(elemsCollapse);
  var instances = M.Modal.init(elemsModal);
});