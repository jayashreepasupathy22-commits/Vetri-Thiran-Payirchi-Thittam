function escapeHtml(value) {
    return String(value ?? "")
        .replace(
            /[&<>'"]/g,
            function (character) {
                return {
                    "&": "&amp;",
                    "<": "&lt;",
                    ">": "&gt;",
                    "'": "&#39;",
                    '"': "&quot;"
                }[character];
            }
        );
}


function renderResult(
    rootId,
    data
) {

    const root =
        document.getElementById(rootId);

    root.className = "result";

    const allocations =
        Object.entries(
            data.budget_allocation || {}
        )
        .map(
            ([key, value]) => `
                <div class="allocation-item">
                    <b>${escapeHtml(key)}</b>
                    <span>
                        ₹${Number(value)
                            .toLocaleString("en-IN")}
                    </span>
                </div>
            `
        )
        .join("");


    const recommendations =
        (data.recommendations || [])
        .map(
            item => `
                <article class="rec">

                    <h3>
                        ${escapeHtml(item.name)}
                    </h3>

                    <span class="pill">
                        ${escapeHtml(item.platform)}
                        ·
                        ${escapeHtml(item.category)}
                    </span>

                    <p>
                        <strong>
                            Estimated:
                        </strong>
                        ₹${Number(
                            item.estimated_price
                        ).toLocaleString("en-IN")}
                    </p>

                    <p>
                        ${escapeHtml(
                            item.reason
                        )}
                    </p>

                    <a
                        href="${escapeHtml(
                            item.search_url
                        )}"
                        target="_blank"
                        rel="noopener noreferrer"
                    >
                        Search platform →
                    </a>

                </article>
            `
        )
        .join("");


    const tips =
        (data.tips || [])
        .map(
            tip => `
                <li>
                    ${escapeHtml(tip)}
                </li>
            `
        )
        .join("");


    root.innerHTML = `

        <div class="card">

            <span class="pill">
                ${escapeHtml(data.source)}
            </span>

            <h2>
                Your plan
            </h2>

            <p>
                ${escapeHtml(data.summary)}
            </p>


            <h3>
                Budget allocation
            </h3>

            <div class="allocation-grid">
                ${allocations}
            </div>


            <h3>
                Recommendations
            </h3>

            <div class="recommendation-grid">
                ${recommendations}
            </div>


            <h3>
                Tips
            </h3>

            <ul>
                ${tips}
            </ul>


            <small>
                ${escapeHtml(
                    data.disclaimer
                )}
            </small>

        </div>
    `;
}


function setupPlanner(
    formId,
    url,
    resultId,
    isMultipart = false
) {

    const form =
        document.getElementById(formId);

    form.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();

            const root =
                document.getElementById(
                    resultId
                );

            root.innerHTML = `
                <div class="card">
                    Generating your plan…
                </div>
            `;


            try {

                let options;


                if (isMultipart) {

                    options = {
                        method: "POST",
                        body: new FormData(form)
                    };

                } else {

                    const data =
                        Object.fromEntries(
                            new FormData(form)
                        );


                    const numberFields = [
                        "budget",
                        "lights",
                        "fans",
                        "dining_tables",
                        "guests"
                    ];


                    numberFields.forEach(
                        function (field) {

                            if (
                                field in data
                            ) {

                                data[field] =
                                    Number(
                                        data[field]
                                    );
                            }
                        }
                    );


                    options = {

                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(data)
                    };
                }


                const response =
                    await fetch(
                        url,
                        options
                    );


                const data =
                    await response.json();


                if (!response.ok) {

                    throw new Error(
                        data.detail ||
                        "Request failed"
                    );
                }


                renderResult(
                    resultId,
                    data
                );


            } catch (error) {

                root.innerHTML = `
                    <div class="card error">
                        ${escapeHtml(
                            error.message
                        )}
                    </div>
                `;
            }
        }
    );
}