M.AutoInit();

document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.sidenav');
    var carousel = document.querySelectorAll('.carousel');
    var elemsSelect = document.querySelectorAll('select');
    var elemsCollapse = document.querySelectorAll('.collapsible');

    var optionsCarousel = {
      padding: 50,
    }

    var instancesSidenav = M.Sidenav.init(elems);
    var instancesCarousel = M.Carousel.init(carousel, optionsCarousel);
    var instancesSelect = M.FormSelect.init(elemsSelect);
    var instancesCollapse = M.Collapsible.init(elemsCollapse);
  });

  const questionsList = document.querySelectorAll('.questions-list')
  const categoryButtons = document.querySelectorAll('.category-buttons')
  const noPosts = document.querySelector('#no-posts')
  let emptyPosts = 0

  categoryButtons.forEach((button) => {
    button.addEventListener('click', (e) => {
      noPosts.classList.add("questions-hide")

      

      emptyPosts = 0

      const x = e.path[0].innerText.toLowerCase();
     
      questionsList.forEach(question => {
       
      if (x == question.dataset.questions.toLowerCase()) {
      
        question.classList.toggle('questions-hide')
      } else {
        question.classList.add('questions-hide')
        emptyPosts++
        if (emptyPosts == questionsList.length) {
          console.log("nothing");
          noPosts.classList.toggle("questions-hide")
        }
      }
    })
    })
  })