const slider = document.getElementById('slider');
    const cards = Array.from(document.querySelectorAll('.card-slider'));
    let currentIndex = 0;
    let lr = 0;

    function updateCardVisibility() {
    if (lr === -1) {
      cards.forEach((card, index) => {
        
          if (index === currentIndex+1) {
            card.classList.remove('in-view');
            card.classList.add('hidden-right');
          } 
          else if(index === currentIndex)
          {
            card.classList.remove('hidden-left');
            card.classList.add('in-view');
          }
      });
    }
    else 
    {
        for (let index = 9; index >= 0; index--) {
            const card = cards[index];
            if (index === currentIndex-1) 
            {
            card.classList.remove('in-view');
            card.classList.add('hidden-left');
            } 
            else if(index === currentIndex)
            {
                card.classList.remove('hidden-right');
                card.classList.remove('in-view');
            }
        }
    }
    const dots = Array.from(document.querySelectorAll('.dot-slider'));
  dots.forEach((dot, index) => {
    if (index === currentIndex) {
      dot.classList.add('active');
    } else {
      dot.classList.remove('active');
    }
  });
    }
    function updateCard_0to9() {
        cards.forEach((card, index) => {
          setTimeout(() => {
            if (index === currentIndex) {
              card.classList.remove('hidden-right');
              card.classList.add('in-view');
            } else if (index === 0) {
              card.classList.remove('in-view');
              card.classList.add('hidden-left');
            } else {
              card.classList.remove('hidden-right');
              card.classList.add('hidden-left');
            }
          }, index * 70); 
        });
        const dots = Array.from(document.querySelectorAll('.dot-slider'));
  dots.forEach((dot, index) => {
    if (index === currentIndex) {
      dot.classList.add('active');
    } else {
      dot.classList.remove('active');
    }
  });
      }
    function updateCard_9to0() {
        for (let index = 9; index >= 0; index--) {
            setTimeout(() => {
              const card = cards[index];
              if (index === currentIndex) {
                card.classList.remove('hidden-left');
                card.classList.add('in-view');
              } else if (index === 9) {
                card.classList.remove('in-view');
                card.classList.add('hidden-right');
              } else {
                card.classList.remove('hidden-left');
                card.classList.add('hidden-right');
              }
            }, (9 - index) * 70); 
          }
        const dots = Array.from(document.querySelectorAll('.dot-slider'));
        dots.forEach((dot, index) => {
           if (index === currentIndex) {
              dot.classList.add('active');
            } else {
          dot.classList.remove('active');
        }
  });
    }

    function slideLeft() {
      if (currentIndex === 0) {
        currentIndex=9
        updateCard_0to9();
        return 0;
      } else {
        currentIndex--;
      }
      lr = -1;
      updateCardVisibility();
    }

    function slideRight() {
      if (currentIndex === 9) {
        currentIndex=0
        updateCard_9to0()
        return 0;

      } else {
        currentIndex++;
      }
      lr = 1;
      updateCardVisibility();
    }

    function redirectToLink(url) {
        window.open(url, "_blank");
      }

    document.addEventListener('keydown', function(event) {
      if (event.key === 'ArrowLeft') {
        slideLeft();
      } else if (event.key === 'ArrowRight') {
        slideRight();
      }
    });