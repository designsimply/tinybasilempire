function search() {
  var search = $('#search');
  search.val('');
  search.focus();
}

// Mousetrap.bind({
//   '/': document.getElementById("search").focus();,
//   't': tweet,
//   '?': function modal() { $('#help').modal('show'); },
//   'j': function next() { highLight('j') },
//   'k': function prev() { highLight('k') },
//   'command+k': function () { alert("command+k"); return false; }
// });

// single keys
Mousetrap.bind('4', function () { console.log('4'); });
Mousetrap.bind('/', function () { document.getElementById("q").focus(); return false; });
Mousetrap.bind("?", function () { alert('show shortcuts!'); });
Mousetrap.bind("h", function () { document.getElementById("home").click(); });
Mousetrap.bind("t", function () { document.getElementById("tags").click(); });
Mousetrap.bind("a", function () { document.getElementById("add").click(); });
Mousetrap.bind("]", function () { document.getElementById("next").click(); });
Mousetrap.bind("[", function () { document.getElementById("previous").click(); });
Mousetrap.bind("j", function () { document.getElementById("next").click(); });
Mousetrap.bind("k", function () { document.getElementById("previous").click(); });
Mousetrap.bind("s h e r i", function () { alert('hello sheri'); });
//Mousetrap.bind('esc', function () { console.log('escape'); }, 'keyup');

// combinations
Mousetrap.bind('command+shift+k', function () { alert('command shift k'); });
Mousetrap.bind('#', function () { alert('# TODO: trigger delete for the active list item'); });

// map multiple combinations to the same callback
Mousetrap.bind(['command+k', 'ctrl+k'], function () {
  console.log('command k or control k');

  // return false to prevent default browser behavior
  // and stop event from bubbling
  return false;
});

// gmail style sequences
Mousetrap.bind('g i', function () { alert('go to inbox'); });
Mousetrap.bind('* a', function () { console.log('select all'); });

// konami code!
Mousetrap.bind('up up down down left right left right b a enter', function () {
  console.log('konami code');
});