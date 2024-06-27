
let sidebarOpen = false;
const sidebar = document.getElementById('sidebar');

function timedPopup(type, message, goto, session_id) {
    let timerInterval;
    Swal.fire({
        title: message,
        icon: type,
        timer: 1500,
        timerProgressBar: true,
        didOpen: () => {
            Swal.showLoading();
        },
        willClose: () => {
            clearInterval(timerInterval);
            document.cookie = `session_id=${session_id};`;
            window.location.href = `/${goto}`;
        }
    }).then((result) => {
        if (result.dismiss === Swal.DismissReason.timer) {
        }
    });
}
function openSidebar() {
    if (!sidebarOpen) {
        sidebar.classList.add('sidebar-responsive');
        sidebarOpen = true;
    }
}
function closeSidebar() {
    if (sidebarOpen) {
        sidebar.classList.remove('sidebar-responsive');
        sidebarOpen = false;
    }
}

function logout(session_id) {

    Swal.fire({
        title: "Are you sure?",
        text: "You want to close this session?",
        icon: "warning",
        showCancelButton: true,

        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Yes"

    }).then((result) => {
        if (result.isConfirmed) {
            fetch('/logout', {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json",
                    "Session-Id": session_id
                },
            }).then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
                .then(data => {
                    document.location.href = '/';
                })
                .catch(error => {
                    console.error('Fetch error:', error);
                });
        }
    });
}

function gotoDashboard(session_id) {
    document.cookie = `session_id=${session_id}`;
    window.location.href = '/dashboard';
}
//Company Functions

function gotoCompanies(session_id) {
    document.cookie = `session_id=${session_id}`;
    window.location.href = '/companies';

}

function gotoAddCompany(session_id) {

    document.cookie = `session_id=${session_id};`;
    window.location.href = "/add_company";
}

function addCompany(event, sessionId) {
    event.preventDefault(); // Prevents the default form submission behavior

    // Fetch the form data
    const formData = new FormData(event.target);

    // Convert form data to JSON object
    const companyData = {};
    formData.forEach((value, key) => {
        companyData[key] = value;
    });

    // Add the session ID to the data
    companyData['session_id'] = sessionId;

    // Make the POST request
    Swal.fire({
        title: "Are you sure?",
        text: "You don't want any further changes?",
        icon: "warning",
        showCancelButton: true,

        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Yes"

    }).then((result) => {
        if (result.isConfirmed) {

            fetch('/add_company', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(companyData),
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        timedPopup("success", data.message, 'companies', sessionId);

                    } else {
                        timedPopup("warning", data.message, 'add_company', sessionId);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });

        }
    });
}

function editCompany(company_id, session_id) {


    fetch(`/edit_company?company_id=${company_id}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Cookie': 'session_id' + `${session_id}`
        }
    })
    document.cookie = `session_id=${session_id};`;
    window.location.href = `/edit_company?company_id=${company_id}`;

}

function deleteCompany(company_id, session_id) {

    Swal.fire({
        title: "Are you sure?",
        text: "You won't be able to revert this!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Yes, delete it!"
    }).then((result) => {
        if (result.isConfirmed) {
            fetch(`/remove_company?company_id=${company_id}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Cookie': `session_id=${session_id}`,
                }
            })
                .then(response => response.json())
                .then(data => {
                    timedPopup("success", data.message, 'companies', session_id);
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        }
    });
}

function updateCompany(event, company_id, session_id) {
    event.preventDefault();

    var formData = {
        company_id: company_id,
        company_name: document.getElementById('company_name').value,
        company_representative: document.getElementById('company_representative').value,
        contact: document.getElementById('contact').value,
        address: document.getElementById('address').value,
    };

    Swal.fire({
        title: "Are you sure?",
        text: "You won't be able to revert this!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Yes, update it!"
    }).then((result) => {
        if (result.isConfirmed) {
            fetch('/edit_company', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Cookie': `session_id=${session_id}`,
                },
                body: JSON.stringify(formData),
            })
                .then(response => response.json())
                .then(data => {
                    timedPopup("success", data.message, 'companies', session_id);
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        }
    });
}

//Clients Functions
function gotoClients(session_id) {
    document.cookie = `session_id=${session_id}`;
    window.location.href = '/clients';

}

function gotoAddClient(session_id) {

    document.cookie = `session_id=${session_id};`;
    window.location.href = "/add_client";
}

function addClient(event, sessionId) {
    event.preventDefault(); // Prevents the default form submission behavior

    // Fetch the form data
    const formData = new FormData(event.target);

    // Convert form data to JSON object
    const clientData = {};
    formData.forEach((value, key) => {
        clientData[key] = value;
    });

    // Add the session ID to the data
    clientData['session_id'] = sessionId;

    // Make the POST request
    Swal.fire({
        title: "Are you sure?",
        text: "You don't want any further changes?",
        icon: "warning",
        showCancelButton: true,

        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Yes"

    }).then((result) => {
        if (result.isConfirmed) {

            fetch('/add_client', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(clientData),
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        timedPopup("success", data.message, 'clients', sessionId);

                    } else {
                        timedPopup("warning", data.message, 'add_client', sessionId);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });

        }
    });
}

function editClient(client_id, session_id) {


    fetch(`/edit_client?client_id=${client_id}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Cookie': 'session_id' + `${session_id}`
        }
    })
    document.cookie = `session_id=${session_id};`;
    window.location.href = `/edit_client?client_id=${client_id}`;

}

function updateClient(event, client_id, session_id) {
    event.preventDefault();

    var formData = {
        client_id: client_id,
        client_name: document.getElementById('client_name').value,
        contact: document.getElementById('contact').value,
        client_since: document.getElementById('client_since').value,
        address: document.getElementById('address').value,
    };

    Swal.fire({
        title: "Are you sure?",
        text: "You won't be able to revert this!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Yes, update it!"
    }).then((result) => {
        if (result.isConfirmed) {
            fetch('/edit_client', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Cookie': `session_id=${session_id}`,
                },
                body: JSON.stringify(formData),
            })
                .then(response => response.json())
                .then(data => {
                    timedPopup("success", data.message, 'clients', session_id);
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        }
    });
}

function deleteClient(client_id, session_id) {

    Swal.fire({
        title: "Are you sure?",
        text: "You won't be able to revert this!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Yes, delete it!"
    }).then((result) => {
        if (result.isConfirmed) {
            fetch(`/remove_client?client_id=${client_id}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Cookie': `session_id=${session_id}`,
                }
            })
                .then(response => response.json())
                .then(data => {
                    timedPopup("success", data.message, 'clients', session_id);
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        }
    });
}

//Products Functions
function gotoProducts(session_id) {
    document.cookie = `session_id=${session_id}`;
    window.location.href = '/products';
}


function gotoAddProduct(session_id) {
    document.cookie = `session_id=${session_id};`;
    window.location.href = "/add_product";
}

function addProduct(event, sessionId) {
    event.preventDefault(); // Prevents the default form submission behavior

    // Fetch the form data
    const formData = new FormData(event.target);

    // Convert form data to JSON object
    const productData = {};
    formData.forEach((value, key) => {
        productData[key] = value;
    });

    // Add the session ID to the data
    productData['session_id'] = sessionId;

    // Make the POST request
    Swal.fire({
        title: "Are you sure?",
        text: "You don't want any further changes?",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Yes"
    }).then((result) => {
        if (result.isConfirmed) {
            fetch('/add_product', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(productData),
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        timedPopup("success", data.message, 'products', sessionId);
                    } else {
                        timedPopup("warning", data.message, 'add_product', sessionId);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        }
    });
}

function setCompany(companyid) {
    document.getElementById('company').value = companyid;
}

function editProduct(product_id, session_id) {
    fetch(`/edit_product?product_id=${product_id}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Cookie': `session_id=${session_id}`,
        }
    })
    document.cookie = `session_id=${session_id};`;
    window.location.href = `/edit_product?product_id=${product_id}`;
}

function deleteProduct(product_id, session_id) {
    Swal.fire({
        title: "Are you sure?",
        text: "You won't be able to revert this!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Yes, delete it!"
    }).then((result) => {
        if (result.isConfirmed) {
            fetch(`/remove_product?product_id=${product_id}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Cookie': `session_id=${session_id}`,
                }
            })
                .then(response => response.json())
                .then(data => {
                    timedPopup("success", data.message, 'products', session_id);
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        }
    });
}

function updateProduct(event, product_id, session_id) {
    event.preventDefault();

    var formData = {
        product_id: product_id,
        product_name: document.getElementById('product_name').value,
        company_id: document.getElementById('company_id').value,
        brand: document.getElementById('brand').value,
        pieces_per_carton: document.getElementById('pieces_per_carton').value,
        price_carton: document.getElementById('price_carton').value,
        selling_price_carton: document.getElementById('selling_price_carton').value,
        current_cartons: document.getElementById('current_cartons').value,
        alarming_stock_level: document.getElementById('alarming_stock_level').value
    };

    Swal.fire({
        title: "Are you sure?",
        text: "You won't be able to revert this!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Yes, update it!"
    }).then((result) => {
        if (result.isConfirmed) {
            fetch('/edit_product', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Cookie': `session_id=${session_id}`,
                },
                body: JSON.stringify(formData),
            })
                .then(response => response.json())
                .then(data => {
                    timedPopup("success", data.message, 'products', session_id);
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        }
    });
}

//Purchase Functions
function gotoPurchases(session_id) {
    document.cookie = `session_id=${session_id}`;
    window.location.href = '/purchases';
}

function gotoAddPurchase(session_id) {
    document.cookie = `session_id=${session_id};`;
    window.location.href = "/add_purchase";
}


function addPurchase(event, sessionId) {
    event.preventDefault(); // Prevents the default form submission behavior

    // Fetch the form data
    const formData = new FormData(event.target);

    // Convert form data to JSON object
    const purchaseData = {};
    formData.forEach((value, key) => {
        purchaseData[key] = value;
    });

    // Add the session ID to the data
    purchaseData['session_id'] = sessionId;

    // Make the POST request
    Swal.fire({
        title: "Are you sure?",
        text: "You don't want any further changes?",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Yes"
    }).then((result) => {
        if (result.isConfirmed) {
            fetch('/add_purchase', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(purchaseData),
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        timedPopup("success", data.message, 'purchases', sessionId);
                    } else {
                        timedPopup("warning", data.message, 'add_purchase', sessionId);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        }
    });
}

function editPurchase(purchase_id, session_id) {
    fetch(`/edit_purchase?purchase_id=${purchase_id}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Cookie': `session_id=${session_id}`,
        }
    })
    document.cookie = `session_id=${session_id};`;
    window.location.href = `/edit_purchase?purchase_id=${purchase_id}`;
}


function updatePurchase(event, purchase_id, session_id) {
    event.preventDefault();

    var formData = {
        purchase_id: purchase_id,
        product_id: document.getElementById('product_id').value,
        purchased_cartons: document.getElementById('purchased_cartons').value,
        purchase_date: document.getElementById('purchase_date').value,
        purchase_amount: document.getElementById('purchase_amount').value,
    };

    Swal.fire({
        title: "Are you sure?",
        text: "You won't be able to revert this!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Yes, update it!"
    }).then((result) => {
        if (result.isConfirmed) {
            fetch('/edit_purchase', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Cookie': `session_id=${session_id}`,
                },
                body: JSON.stringify(formData),
            })
                .then(response => response.json())
                .then(data => {
                    // Assuming you have a function timedPopup for displaying success messages
                    timedPopup("success", data.message, 'purchases', session_id);
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        }
    });
}


function deletePurchase(purchase_id, session_id) {
    Swal.fire({
        title: "Are you sure?",
        text: "You won't be able to revert this!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Yes, delete it!"
    }).then((result) => {
        if (result.isConfirmed) {
            fetch(`/remove_purchase?purchase_id=${purchase_id}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Cookie': `session_id=${session_id}`,
                }
            })
                .then(response => response.json())
                .then(data => {
                    timedPopup("success", data.message, 'purchases', session_id);
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        }
    });
}

//Sales Functions
function gotoSales(session_id) {
    document.cookie = `session_id=${session_id}`;
    window.location.href = '/sales';
}

function gotoAddSales(session_id) {
    document.cookie = `session_id=${session_id};`;
    window.location.href = "/add_sale";
}


function addSales(event, sessionId) {
    event.preventDefault();
    const formData = new FormData(event.target);

    const salesData = {};
    formData.forEach((value, key) => {
        salesData[key] = value;
    });

    salesData['session_id'] = sessionId;
    console.log(salesData);

    Swal.fire({
        title: "Are you sure?",
        text: "You don't want any further changes?",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Yes"
    }).then((result) => {
        if (result.isConfirmed) {
            fetch('/add_sale', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(salesData),
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        console.log(salesData);
                        timedPopup("success", data.message, 'sales', sessionId);
                    } else {
                        console.log(salesData);
                        timedPopup("warning", data.message, 'add_sale', sessionId);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        }
    }
    );
}

function editSales(sale_id, session_id) {
    fetch(`/edit_sale?sale_id=${sale_id}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Cookie': `session_id=${session_id}`,
        }
    })
    document.cookie = `session_id=${session_id};`;
    window.location.href = `/edit_sale?sale_id=${sale_id}`;
}

function updateSales(event, sale_id, session_id) {
    event.preventDefault();

    const formData = new FormData(event.target);

    const updatedsaleData = {};
    formData.forEach((value, key) => {
        updatedsaleData[key] = value;
    });

    updatedsaleData['sale_id'] = sale_id;

    Swal.fire({
        title: "Are you sure?",
        text: "You won't be able to revert this!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Yes, update it!"
    }).then((result) => {
        if (result.isConfirmed) {
            fetch('/edit_sale', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Cookie': `session_id=${session_id}`,
                },
                body: JSON.stringify(updatedsaleData),
            })
                .then(response => response.json())
                .then(data => {
                    // Assuming you have a function timedPopup for displaying success messages
                    timedPopup("success", data.message, 'sales', session_id);
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        }
    });
}


function deleteSales(sale_id, session_id) {
    Swal.fire({
        title: "Are you sure?",
        text: "You won't be able to revert this!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Yes, delete it!"
    }).then((result) => {
        if (result.isConfirmed) {
            fetch(`/remove_sale?sale_id=${sale_id}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Cookie': `session_id=${session_id}`,
                }
            })
                .then(response => response.json())
                .then(data => {
                    timedPopup("success", data.message, 'sales', session_id);
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        }
    });
}

function goBack() {
    window.history.back();
}

// ---------- CHARTS ----------

// BAR CHART
const barChartOptions = {
    series: [
        {
            data: [10, 8, 6, 4, 2],
        },
    ],
    chart: {
        type: 'bar',
        height: 350,
        toolbar: {
            show: false,
        },
    },
    colors: ['#246dec', '#cc3c43', '#367952', '#f5b74f', '#4f35a1'],
    plotOptions: {
        bar: {
            distributed: true,
            borderRadius: 4,
            horizontal: false,
            columnWidth: '40%',
        },
    },
    dataLabels: {
        enabled: false,
    },
    legend: {
        show: false,
    },
    xaxis: {
        categories: ['Laptop', 'Phone', 'Monitor', 'Headphones', 'Camera'],
    },
    yaxis: {
        title: {
            text: 'Count',
        },
    },
};

const barChart = new ApexCharts(
    document.querySelector('#bar-chart'),
    barChartOptions
);
barChart.render();

// AREA CHART
const areaChartOptions = {
    series: [
        {
            name: 'Purchase Orders',
            data: [31, 40, 28, 51, 42, 109, 100],
        },
        {
            name: 'Sales Orders',
            data: [11, 32, 45, 32, 34, 52, 41],
        },
    ],
    chart: {
        height: 350,
        type: 'area',
        toolbar: {
            show: false,
        },
    },
    colors: ['#4f35a1', '#246dec'],
    dataLabels: {
        enabled: false,
    },
    stroke: {
        curve: 'smooth',
    },
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
    markers: {
        size: 0,
    },
    yaxis: [
        {
            title: {
                text: 'Purchase Orders',
            },
        },
        {
            opposite: true,
            title: {
                text: 'Sales Orders',
            },
        },
    ],
    tooltip: {
        shared: true,
        intersect: false,
    },
};

const areaChart = new ApexCharts(
    document.querySelector('#area-chart'),
    areaChartOptions
);
areaChart.render();

document.addEventListener("DOMContentLoaded", function () {
    var cards = document.querySelectorAll(".card");

    cards.forEach(function (card, index) {
        var colors = ['#246dec', '#f5b74f', '#367952', '#cc3c43'];
        card.style.borderLeft = "7px solid " + colors[index % colors.length];
    });
});