function search() {
  var search = $("#search");
  search.val("");
  search.focus();
}
// Keyboard shortcut help overlay
document.addEventListener('DOMContentLoaded', () => {
  // Create the overlay container
  const overlay = document.createElement('div');
  overlay.id = 'overlay';
  document.body.appendChild(overlay);

  // Create the text element
  const overlayText = document.createElement('div');
  overlayText.id = 'overlay-text';
  overlayText.textContent = `  
    h - Home
    l - Latest
    t - Tags
    a - Add
    o - Open
    e - Edit
    i - Item
    # - Delete
    n - Next page
    p - Previous page
    j - Next item
    k - Previous item
    + - Increase limit by 20
    o o - Open All
    cmd+e - Edit All
    cr - remove querystring
    cl - copy link
    cc - copy title & link
    cd - copy title, link, & description
    command+enter - Submit
  `;
  overlay.appendChild(overlayText);

  // Add CSS styles for the overlay and text
  const style = document.createElement('style');
  style.textContent = `
    #overlay {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background-color: rgba(0, 0, 0, 0.7); /* Semi-transparent background */
      display: flex;
      justify-content: center;
      align-items: center;
      z-index: 9999; /* Ensure it's on top */
    }
    #overlay-text {
      color: white;
      font-size: 1.5rem;
      text-align: center;
      white-space: pre; /* Preserve line breaks and spaces */
    }
  `;
  document.head.appendChild(style);
  document.getElementById("overlay").style.display = "none";
});
Mousetrap.bind("?", function () {
  if (document.getElementById("overlay").style.display === "block") {
    document.getElementById("overlay").style.display = "none";
  } else {
    document.getElementById("overlay").style.display = "block";
  }
});

// single keys
Mousetrap.bind("/", function () {
  document.getElementById("q").focus();
  document.getElementById("q").select();
  return false;
});
Mousetrap.bind("h", function () {
  document.getElementById("home").click();
});
Mousetrap.bind("l", function () {
  document.getElementById("latest").click();
});
Mousetrap.bind("t", function () {
  document.getElementById("tags").click();
});
Mousetrap.bind("a", function () {
  document.getElementById("add").click();
});
Mousetrap.bind("o", function () {
  document
    .getElementsByClassName("current")[0]
    .getElementsByClassName("link")[0]
    .click();
});
Mousetrap.bind("e", function () {
  document
    .getElementsByClassName("current")[0]
    .getElementsByClassName("edit")[0]
    .click();
});
Mousetrap.bind("i", function () {
  document
    .getElementsByClassName("current")[0]
    .getElementsByClassName("date")[0]
    .getElementsByTagName("a")[0]
    .click();
});
const url = window.location.href;
if (url.includes("/edit") || url.includes("/add")) {
  Mousetrap.bindGlobal("c r", function () {
    event.preventDefault(); // Prevents the second letter from being typed
    document.getElementById("remove-querystring").click();
  });
  Mousetrap.bindGlobal("c l", function () {
    event.preventDefault(); // Prevents the second letter from being typed
    document.getElementById("copy-link").click();
  });
  Mousetrap.bindGlobal("c c", function (event) {
    event.preventDefault(); // Prevents the second letter from being typed
    document.getElementById("copy-title-and-link").click();
  });
  Mousetrap.bindGlobal("c d", function () {
    event.preventDefault(); // Prevents the second letter from being typed
    document.getElementById("copy-all").click();
  });  
} else {
  Mousetrap.bind("c l", function () {
    navigator.clipboard.writeText(
      document
        .getElementsByClassName("current")[0]
        .getElementsByClassName("link")[0].href
    );
  });  
  Mousetrap.bind("c c", function () {
    navigator.clipboard.writeText(
      document
        .getElementsByClassName("current")[0]
        .getElementsByClassName("link")[0].innerText +
        " " +
        document
          .getElementsByClassName("current")[0]
          .getElementsByClassName("link")[0].href
    );
  });
  Mousetrap.bind("c d", function () {
    navigator.clipboard.writeText(
      document
        .getElementsByClassName("current")[0]
        .getElementsByClassName("link")[0].innerText +
        " " +
        document
          .getElementsByClassName("current")[0]
          .getElementsByClassName("link")[0].href +
          " " +
        document
        .getElementsByClassName("current")[0]
        .getElementsByClassName("description")[0].innerText
    );
  });
}
Mousetrap.bind("+", function () {
  const params = new URLSearchParams(window.location.search);
  const limit = params.get("limit");
  if (limit) {
    document.location = window.location.href.replace(limit, Number(limit) + 20);
  } else {
    document.location = window.location.href + "?limit=20";
  }
});
Mousetrap.bind("#", function () {
  if (typeof document.getElementsByClassName("current")[0] !== "undefined") {
    document
      .getElementsByClassName("current")[0]
      .getElementsByClassName("delete")[0]
      .click();
  }
  if (typeof document.getElementById("delete") !== "undefined") {
    document.getElementById("delete").click();
  }
});
Mousetrap.bind("s h e r i", function () {
  alert("hello sheri");
});
Mousetrap.bind("d y l a n", function () {
  alert("hello dylan");
});
Mousetrap.bind("j", function () {
  cur = document.getElementsByClassName("item");
  if (typeof list === "undefined") {
    list = document.getElementsByClassName("item");
  }
  if (typeof i === "undefined") {
    i = 0;
  }
  if (i >= 0) {
    if (i >= list.length) {
      list[i - 1].classList.remove("current");
      i = 0;
    }
    if (list[i - 1]) {
      list[i - 1].classList.remove("current");
    }
    if (list[i]) {
      list[i].classList.add("current");
    }
    document
      .getElementsByClassName("current")[0]
      .getElementsByClassName("link")[0]
      .focus();
    i++;
  }
});
Mousetrap.bind("k", function () {
  if (typeof list === "undefined") {
    list = document.getElementsByClassName("item");
  }
  if (typeof i === "undefined") {
    i = list.length;
  }
  if (i >= 0) {
    i--;
    if (i < 0) {
      list[i + 1].classList.remove("current");
      i = list.length - 1;
    }
    if (list[i + 1]) {
      list[i + 1].classList.remove("current");
    }
    if (list[i]) {
      list[i].classList.add("current");
    }
    document
      .getElementsByClassName("current")[0]
      .getElementsByClassName("link")[0]
      .focus();
  }
});
//Mousetrap.bind('esc', function () { console.log('escape'); }, 'keyup');

// key combinations
Mousetrap.bind("o o", function () {
  links = document.getElementsByClassName("link");
  if (typeof links !== "undefined") {
    for (i = 0; i < links.length; i++) {
      window.open(links[i].href);
    }
  }
});
Mousetrap.bind("command+e", function () {
  links = document.getElementsByClassName("edit");
  if (typeof links !== "undefined") {
    for (i = 0; i < links.length; i++) {
      window.open(links[i].href);
    }
  }
});
Mousetrap.bindGlobal("command+enter", function () {
  document.activeElement.closest("form").submit();
});

// map multiple combinations to the same callback
// return false to prevent default browser behavior and stop event bubbling
Mousetrap.bind(["n", "]"], function () {
  document.getElementById("next").click();
  return false;
});
Mousetrap.bind(["p", "["], function () {
  document.getElementById("previous").click();
  return false;
});

// gmail style sequences
Mousetrap.bind("g i", function () {
  document.getElementById("home").click();
});
Mousetrap.bind("* a", function () {
  console.log("select all");
});

// konami code!
Mousetrap.bind("up up down down left right left right b a enter", function () {
  console.log("You did it!");
});