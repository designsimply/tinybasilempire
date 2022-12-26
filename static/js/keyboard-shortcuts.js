function search() {
  var search = $('#search');
  search.val('');
  search.focus();
}

// single keys
Mousetrap.bind('/', function () { document.getElementById("q").focus(); document.getElementById("q").select(); return false; });
Mousetrap.bind("?", function () { alert('TODO: show Keyboard Shortcuts Overlay'); });
Mousetrap.bind("h", function () { document.getElementById('home').click(); });
Mousetrap.bind("l", function () { document.getElementById('latest').click(); });
Mousetrap.bind("t", function () { document.getElementById('tags').click(); });
Mousetrap.bind("a", function () { document.getElementById('add').click(); });
Mousetrap.bind("o", function () { document.getElementsByClassName('current')[0].getElementsByClassName('link')[0].click(); });
Mousetrap.bind("e", function () { document.getElementsByClassName('current')[0].getElementsByClassName('edit')[0].click(); });
Mousetrap.bind("i", function () { document.getElementsByClassName('current')[0].getElementsByClassName('date')[0].getElementsByTagName('a')[0].click(); });
Mousetrap.bind("#", function () {
  if (typeof document.getElementsByClassName('current')[0] !== 'undefined') {
    document.getElementsByClassName('current')[0].getElementsByClassName('delete')[0].click();
  }
  if (typeof document.getElementById('delete') !== 'undefined') {
    document.getElementById('delete').click();
  }
});
Mousetrap.bind("s h e r i", function () { alert('hello sheri'); });
Mousetrap.bind("d y l a n", function () { alert('hello dylan'); });
Mousetrap.bind("j", function () {
  cur = document.getElementsByClassName('item');
  if (typeof list === 'undefined') { list = document.getElementsByClassName('item'); }
  if (typeof i === 'undefined') { i = 0; }
  if (i >= 0) {
    if (i >= list.length) { list[i - 1].classList.remove('current'); i = 0; }
    if (list[i - 1]) { list[i - 1].classList.remove('current'); };
    if (list[i]) { list[i].classList.add('current'); }
    document.getElementsByClassName('current')[0].getElementsByClassName('link')[0].focus();
    i++;
  }
});
Mousetrap.bind("k", function () {
  if (typeof list === 'undefined') { list = document.getElementsByClassName('item'); }
  if (typeof i === 'undefined') { i = list.length; }
  if (i >= 0) {
    i--;
    if (i < 0) { list[i + 1].classList.remove('current'); i = list.length - 1; }
    if (list[i + 1]) { list[i + 1].classList.remove('current'); };
    if (list[i]) { list[i].classList.add('current'); }
    document.getElementsByClassName('current')[0].getElementsByClassName('link')[0].focus();
  }
});
//Mousetrap.bind('esc', function () { console.log('escape'); }, 'keyup');

// key combinations
Mousetrap.bind('command+shift+o', function () { links = document.getElementsByClassName('link'); if (typeof links !== 'undefined') { for (i = 0; i < links.length; i++) { window.open(links[i].href); } } });

// map multiple combinations to the same callback
// return false to prevent default browser behavior and stop event bubbling
Mousetrap.bind(['n', ']'], function () { document.getElementById('next').click(); return false; });
Mousetrap.bind(['p', '['], function () { document.getElementById('previous').click(); return false; });

// gmail style sequences
Mousetrap.bind('g i', function () { document.getElementById('home').click(); });
Mousetrap.bind('* a', function () { console.log('select all'); });

// konami code!
Mousetrap.bind('up up down down left right left right b a enter', function () {
  console.log('You did it!');
});