window.onload = function() {
    var firstImage = document.getElementById("secondImage");
    var secondImage = document.getElementById("firstImage");

    function showFirstImage() {
        secondImage.style.display = "none";
        firstImage.style.transform="translate(-50%, -50%) translateX(-280px);"
        firstImage.style.display = "block";
        setTimeout(showSecondImage, 1300);
    }

    function showSecondImage() {
        firstImage.style.display = "none";
        secondImage.style.transform="translate(-50%, -50%) translateX(120px);"
        secondImage.style.display = "block";
        setTimeout(showFirstImage, 1300);
    }
    setTimeout(showFirstImage, 50);
};


var text = "거의 다 됐어 ! 조~ 금만 기다려줘 !";
var text2 = "거의 다 됐어 ! 조~ 금만 기다려줘 !";
var delay = 150;
var showDuration = 300; // 텍스트가 보여지는 시간
var hideDuration = 1000; // 텍스트가 사라지는 시간

var container = document.getElementById("textContainer");
var index = 0;

var countContainer = document.getElementById("countContainer");
var count = 9;

function showNextNumber() {
  if (count >= 0) {
    countContainer.textContent = count;
    count--;
    setTimeout(showNextNumber, 1000);
  }
}

showNextNumber();

function showNextLetter() {
  if (index < text.length) {
    container.textContent += text[index];
    index++;
    setTimeout(showNextLetter, delay);
  } else {
    setTimeout(hideText, showDuration);
  }
}

function hideText() {
  setTimeout(function() {
    container.textContent = "";
    index = 0;
    showNextLetter();
  }, hideDuration);
}

showNextLetter();




setTimeout(function() {
     window.location.href = '/result';
}, 9000); // 9초 대기 후 리디렉션
