const body = document.querySelector("body");
const darkLight = document.querySelector("#darkLight");
const sidebar = document.querySelector(".sidebar");
const submenuItems = document.querySelectorAll(".submenu_item");
const sidebarOpen = document.querySelector("#sidebarOpen");
const sidebarClose = document.querySelector(".collapse_sidebar");
const sidebarExpand = document.querySelector(".expand_sidebar");
sidebarOpen.addEventListener("click", () => sidebar.classList.toggle("close"));
sidebarClose.addEventListener("click", () => {
  sidebar.classList.add("close", "hoverable");
});

sidebarExpand.addEventListener("click", () => {
  sidebar.classList.remove("close", "hoverable");
});

sidebar.addEventListener("mouseenter", () => {
  if (sidebar.classList.contains("hoverable")) {
    sidebar.classList.remove("close");
  }
});

sidebar.addEventListener("mouseleave", () => {
  if (sidebar.classList.contains("hoverable")) {
    sidebar.classList.add("close");
  }
});

submenuItems.forEach((item, index) => {
  item.addEventListener("click", () => {
    item.classList.toggle("show_submenu");
    submenuItems.forEach((item2, index2) => {
      if (index !== index2) {
        item2.classList.remove("show_submenu");
      }
    });
  });
});

if (window.innerWidth < 768) {
  sidebar.classList.add("close");
} else {
  sidebar.classList.remove("close");
}


function closeOpenDropdowns(e) {
	let openDropdownEls = document.querySelectorAll("details.dropdown[open]");

	if (openDropdownEls.length > 0) {
		// If we're clicking anywhere but the summary element, close dropdowns
		if (e.target.parentElement.nodeName.toUpperCase() !== "SUMMARY") {
			openDropdownEls.forEach((dropdown) => {
				dropdown.removeAttribute("open");
			});
		}
	}
}

document.addEventListener("click", closeOpenDropdowns);


$(document).ready(function() {
    $(".notification-drop .item").on('click',function() {
      $(this).find('ul').toggle();
    });
  });

  function filterTable() {
    var filter = document.getElementById("filterDropdown").value.toUpperCase();
    var table = document.getElementById("recent-timein-table");
    var tr = table.getElementsByTagName("tr");

    for (var i = 0; i < tr.length; i++) {
      var td = tr[i].getElementsByTagName("td")[0];
      if (td) {
        var txtValue = td.textContent || td.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
          tr[i].style.display = "";
        } else {
          tr[i].style.display = "none";
        }
      }
    }
}

const searchBtn = document.querySelector('.content nav form .form-input button');
const searchBtnIcon = document.querySelector('.content nav form .form-input button .bx');
const searchForm = document.querySelector('.content nav form');

searchBtn.addEventListener('click', function (e) {
    if (window.innerWidth < 576) {
        e.preventDefault;
        searchForm.classList.toggle('show');
        if (searchForm.classList.contains('show')) {
            searchBtnIcon.classList.replace('bx-search', 'bx-x');
        } else {
            searchBtnIcon.classList.replace('bx-x', 'bx-search');
        }
    }
});

window.addEventListener('resize', () => {
    if (window.innerWidth < 768) {
        sideBar.classList.add('close');
    } else {
        sideBar.classList.remove('close');
    }
    if (window.innerWidth > 576) {
        searchBtnIcon.classList.replace('bx-x', 'bx-search');
        searchForm.classList.remove('show');
    }
});
document.getElementById('export-excel').addEventListener('click', function () {
    exportToExcel('recent-timein-table');
});

function exportToExcel(tableId) {
    /* Get table HTML code */
    var tableHTML = document.getElementById(tableId).outerHTML;

    /* Create a Blob with the HTML content */
    var blob = new Blob([tableHTML], {
        type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    });

    /* Create a download link */
    var a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'recent-timein.xlsx';

    /* Append the link to the body and click it to trigger the download */
    document.body.appendChild(a);
    a.click();

    /* Remove the link from the body */
    document.body.removeChild(a);
}


// Function to export the table to Excel
function exportToExcel() {
    const table = document.querySelector('table');
    const ws = XLSX.utils.table_to_sheet(table);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Sheet1');
    XLSX.writeFile(wb, 'table.xlsx');
}
function filterTable() {
    const dropdown = document.getElementById('filterDropdown');
    const selectedFilter = dropdown.value;

    const rows = document.querySelectorAll('#recent-timein-table tbody tr');
    const sortedRows = Array.from(rows);

    if (selectedFilter === 'az') {
        sortedRows.sort((a, b) => {
            const textA = a.children[0].textContent.toLowerCase();
            const textB = b.children[0].textContent.toLowerCase();
            return textA.localeCompare(textB);
        });
    } else if (selectedFilter === 'za') {
        sortedRows.sort((a, b) => {
            const textA = a.children[0].textContent.toLowerCase();
            const textB = b.children[0].textContent.toLowerCase();
            return textB.localeCompare(textA);
        });
    }

    const tbody = document.querySelector('#recent-timein-table tbody');
    tbody.innerHTML = '';

    sortedRows.forEach(row => {
        tbody.appendChild(row);
    });
}

function searchTable() {
    const searchInput = document.getElementById('searchInput');
    const searchText = searchInput.value.toLowerCase();

    const rows = document.querySelectorAll('#recent-timein-table tbody tr');

    rows.forEach(row => {
        const coachName = row.children[0].textContent.toLowerCase();

        if (coachName.includes(searchText)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
};

