let search_form = document.getElementById("search_form");
let search_buttons = document.getElementsByClassName("page-link");

let message = document.querySelector(".alert");
let xButton = document.querySelector(".alert__close");

let tags = document.getElementsByClassName("project-tag");

let checkboxes = document.querySelectorAll('.message-delete');
let messageDeleteBtn = document.querySelector('.delete-btn');

if (search_form) {
  for (let i = 0; i < search_buttons.length; i++) {
    search_buttons[i].addEventListener("click", function (e) {
      e.preventDefault();

      // Getting page value
      let page_value = this.dataset.page;

      // Adding input field to a form
      search_form.innerHTML += `<input name="page" value="${page_value}" hidden>`;

      // Submitting a form
      search_form.submit();
    });
  }
}


// Tag remove section START
function removeTags(tags) {
  for (let i = 0; i < tags.length; i++) {
    tags[i].addEventListener("click", (e) => {
      let tagId = e.target.dataset.tag;
      let projectId = e.target.dataset.project;

      fetch("https://devsearch-find-developers.herokuapp.com/api/remove-tag/", {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ project: projectId, tag: tagId }),
      })
        .then((response) => response.json())
        .then((data) => {
          e.target.remove();
        });
    });
  }
}

let tagField = document.querySelector("#id__newtags");

function addTag() {
  let tag = tagField.value;

  let lastSym = tag[tag.length - 1];
  if (lastSym === " " || lastSym === ",") {
    let tags = document.getElementsByClassName("project-tag");
    let projectId = tagField.dataset.project;
    fetch("https://devsearch-find-developers.herokuapp.com/api/add-tag/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ project: projectId, tag: tagField.value }),
    })
      .then((response) => response.json())
      .then((data) => {
        let tagsContainer = document.querySelector("#tags-container");
        if (data.tag && data.project) {
          tagsContainer.innerHTML += `
                            <div class="project-tag tag tag--pill tag--main" data-tag="${data.tag.id
            }" data-project="${data.project.id}">
                                ${data.tag.name.toUpperCase()} &#215;
                            </div>
                        `;
          removeTags(tags);
        }
      });
    tagField.value = "";
  }
}

if (xButton) {
  xButton.addEventListener("click", () => {
    message.style = "display: none";
  });
}

removeTags(tags);
// Tag remove section END

// comment delete section START
function enableDeleteBtn(checkboxes) {
  let checkedStatus = false
  let checkedMessages = document.querySelectorAll('.message-delete');
  for (let i = 0; i < checkedMessages.length; i++) {
    if (checkedMessages[i].checked) {
      checkedStatus = true
    }
  }
  if (checkedStatus) {
    messageDeleteBtn.disabled = false;
  }
  else {
    messageDeleteBtn.disabled = true;
  }
}

for (let i = 0; i < checkboxes.length; i++) {
  checkboxes[i].addEventListener('change', function (e) {
    let messageId = e.target.dataset.message;
    enableDeleteBtn(checkboxes)
  })
}
if (messageDeleteBtn) {
  messageDeleteBtn.addEventListener('click', function () {
    let deletingMessagesList = [];
    let profile;
    let deletingMessages = document.querySelectorAll('.message-delete');
    for (let i = 0; i < deletingMessages.length; i++) {
      if (deletingMessages[i].checked) {
        deletingMessagesList.push(deletingMessages[i].dataset.message)
        profile = deletingMessages[i].dataset.profile

      }
    }
    // TODO replace localhost
    fetch("http://localhost:8000/api/remove-message/", {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        messages: deletingMessagesList,
        profile: profile
      }),
    })
      .then(response => response.json())
      .then(data => {
        console.log('Deleted!');
      });
    window.location.reload()
  })
}
// comment delete section END

// Like and Dislike Section START
const rates = document.querySelectorAll('.rate');

if (rates) {
  for (let i = 0; i < rates.length; i++) {
    rates[i].addEventListener('click', (e) => {
      const value = e.target.dataset.value;
      const profileID = e.target.dataset.userid;
      const projectID = e.target.dataset.projectid;
      const redirectUrl = e.target.dataset.redirect;
      if (!profileID) window.location.replace(redirectUrl);
      else {
        // TODO replace localhost
        fetch('http://localhost:8000/api/vote/', {
          method: 'PUT',
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            value,
            profileID,
            projectID
          })
        })
          .then(response => response.json())
          .then(data => {
            const {is_liked, likes, dislikes} = data;
            if (is_liked) {
              document.querySelector('.like').classList.add('selected');
              document.querySelector('.dislike').classList.remove('selected');
            }
            else {
              document.querySelector('.dislike').classList.add('selected');
              document.querySelector('.like').classList.remove('selected');
            }
            document.querySelector('.likes').textContent = likes;
            document.querySelector('.dislikes').textContent = dislikes;
          })
      }

    })
  }
}

// Like and Dislike section END

