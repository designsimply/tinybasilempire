// give a visual indicator if we're not on the production server
if (window.location.hostname != 'tinybasilempire.com') {
    var devnotice = document.head.appendChild(document.createElement("style"));
    devnotice.innerHTML = "html { border-top: 1rem solid mediumseagreen; } html:before { content: '" + window.location.hostname + "'; color: white; background: mediumseagreen; font-size: 1rem; padding: 0 1em 0.25em 1em; right: 0; position: absolute; }";
}
