document.addEventListener(
    "DOMContentLoaded",
    async () => {

        const queryBox =
            document.getElementById("query");

        const submitBtn =
            document.getElementById("submitBtn");

        const clearBtn =
            document.getElementById("clearBtn");

        const copyBtn =
            document.getElementById("copyBtn");

        const responseBox =
            document.getElementById("response");

        const loading =
            document.getElementById("loading");

        const agentInfo =
            document.getElementById("agentInfo");

        const quickActions =
            document.querySelectorAll(".quick-action");


        // ==========================================
        // Load Agent Information
        // ==========================================

        async function loadAgentInfo() {

            try {

                const response =
                    await fetch("/agent_info");

                const data =
                    await response.json();

                agentInfo.innerHTML =
                    `
                    <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:15px;">

                        <div style="padding:12px;background:#f8fafc;border-radius:10px;">
                            <strong>Agent</strong><br>
                            ${data.agent_name}
                        </div>

                        <div style="padding:12px;background:#f8fafc;border-radius:10px;">
                            <strong>Model</strong><br>
                            ${data.model}
                        </div>

                        <div style="padding:12px;background:#f8fafc;border-radius:10px;">
                            <strong>Database</strong><br>
                            ${data.database}
                        </div>

                        <div style="padding:12px;background:#f8fafc;border-radius:10px;">
                            <strong>Vector Store</strong><br>
                            ${data.vector_store}
                        </div>

                    </div>
                    `;

            } catch (error) {

                console.error(error);

                agentInfo.innerHTML =
                    `
                    <div style="color:red;">
                        Unable to load agent information.
                    </div>
                    `;
            }
        }


        // ==========================================
        // Quick Actions
        // ==========================================

        quickActions.forEach(
            button => {

                button.addEventListener(
                    "click",
                    () => {

                        queryBox.value =
                            button.dataset.query;

                        queryBox.focus();
                    }
                );

            }
        );


        // ==========================================
        // Submit Analysis Request
        // ==========================================

        submitBtn.addEventListener(
            "click",
            async () => {

                const query =
                    queryBox.value.trim();

                if (!query) {

                    alert(
                        "Please enter a query."
                    );

                    return;
                }

                loading.classList.remove(
                    "hidden"
                );

                responseBox.innerHTML =
                    `
                    <div style="color:#64748b;">
                        Initializing analysis...
                    </div>
                    `;

                try {

                    const response =
                        await fetch(
                            "/main/chat",
                            {
                                method: "POST",

                                headers: {
                                    "Content-Type":
                                        "application/json"
                                },

                                body: JSON.stringify({
                                    query: query
                                })
                            }
                        );

                    const data =
                        await response.json();

                    if (!response.ok) {

                        throw new Error(
                            data.detail ||
                            "Request failed"
                        );
                    }

                    const formattedResponse =
                        (data.response || "")
                            .replace(/\n/g, "<br>");

                    responseBox.innerHTML =
                        formattedResponse;

                } catch (error) {

                    console.error(error);

                    responseBox.innerHTML =
                        `
                        <div style="color:red;">
                            <strong>Error:</strong><br>
                            ${error.message}
                        </div>
                        `;
                }

                finally {

                    loading.classList.add(
                        "hidden"
                    );
                }

            }
        );


        // ==========================================
        // Clear Button
        // ==========================================

        clearBtn.addEventListener(
            "click",
            () => {

                queryBox.value = "";

                responseBox.innerHTML =
                    `
                    Ready for analysis.
                    `;
            }
        );


        // ==========================================
        // Copy Response
        // ==========================================

        copyBtn.addEventListener(
            "click",
            async () => {

                try {

                    await navigator.clipboard.writeText(
                        responseBox.innerText
                    );

                    const originalText =
                        copyBtn.innerText;

                    copyBtn.innerText =
                        "Copied";

                    setTimeout(
                        () => {

                            copyBtn.innerText =
                                originalText;

                        },
                        1500
                    );

                } catch (error) {

                    console.error(error);

                    alert(
                        "Unable to copy response."
                    );
                }

            }
        );


        // ==========================================
        // Initial Page Load
        // ==========================================

        await loadAgentInfo();

    }
);