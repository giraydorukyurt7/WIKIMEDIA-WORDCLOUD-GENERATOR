async function generateTitle() {
    const pageNo = document.getElementById("pageNo").value;
    const isALL = document.getElementById("isALL").checked;
    const titleSize = document.getElementById("titleSize").value || 3;

    try {
        const response = await fetch("/generate-title", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                pageNo: parseInt(pageNo),
                isALL: isALL,
                titleSize: parseInt(titleSize)
            })
        });

        if (!response.ok) {
            throw new Error("Network response was not ok");
        }

        const data = await response.json();
        document.getElementById("result").innerText = `Title: ${data.title}`;
    } catch (error) {
        console.error("Error:", error);
        document.getElementById("result").innerText = "Error generating title!";
    }
}

async function getPage() {
    const pageNo = document.getElementById("pagePageNo").value;
    const cleanPage = document.getElementById("cleanPage").checked;

    try {
        const response = await fetch("/get-page", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                pageNo: parseInt(pageNo),
                cleanPage: cleanPage
            })
        });

        if (!response.ok) {
            throw new Error("Network response was not ok");
        }

        const data = await response.json();
        document.getElementById("pageResult").innerText = `Page: ${data.Page}`;
    } catch (error) {
        console.error("Error:", error);
        document.getElementById("pageResult").innerText = "Error getting page!";
    }
}