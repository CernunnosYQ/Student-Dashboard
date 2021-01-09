const _C = document.querySelector('.c-schedule');

let i = 0;
let x0 = null;

_C.style.setProperty('--i', i)

function lock(e) {
  x0 = e.changedTouches[0].clientX;
};

function move(e) {
  if (x0) {
    let dx = e.changedTouches[0].clientX - x0;

    if (Math.abs(dx) >= 50) {
      s = Math.sign(dx);

      if ((i > 0 || s < 0) && (i < 4 || s > 0))
        _C.style.setProperty('--i', i -= s);
    }

    x0 = null;
  }
};

_C.addEventListener('touchstart', lock, false);

_C.addEventListener('touchend', move, false);
