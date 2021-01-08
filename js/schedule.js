const _C = document.querySelector('.c-schedule__nested-container');
const _next = document.getElementById('next'),
  _prev = document.getElementById('prev');

_next.addEventListener('click', next);
_prev.addEventListener('click', previous);

let i = 0;
_C.style.setProperty('--i', i);

function next() {
  if (i < 4) {
    _C.style.setProperty('--i', i += 1)
  }
}

function previous() {
  if (i > 0) {
    _C.style.setProperty('--i', i -= 1)
  }
}