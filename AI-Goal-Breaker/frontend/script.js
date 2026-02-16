// CREATE GOAL

const goalForm = document.getElementById("goalForm");

goalForm.addEventListener("submit", async (e) => 
{
    e.preventDefault();

    const goalInput = document.getElementById("goalInput").value.trim();

    const difficulty = document.getElementById("difficultySelect").value;

    if (!goalInput) 
        return;

    const res = await fetch("http://127.0.0.1:5000/create-goal", 
    {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ goal: goalInput, difficulty })
    });


    const data = await res.json();

    if (res.status === 201) 
    {
        document.getElementById("goalInput").value = "";
        loadGoals();
    } 
    else 
    {
        alert(data.error || "Failed to create goal");
    }
});



// LOAD GOALS
async function loadGoals() 
{
    const container = document.getElementById("goalsContainer");
    container.innerHTML = "Loading...";

    const res = await fetch("http://127.0.0.1:5000/goals");
    const data = await res.json();

    if (!Array.isArray(data) || data.length === 0) 
    {
        container.innerHTML = "<p>No goals yet. Add one above!</p>";
        return;
    }

    container.innerHTML = "";

    data.forEach(task => 
    {
        const goalDiv = document.createElement("div");
        goalDiv.className = `goal ${task.difficulty || 'medium'}`;

        goalDiv.innerHTML = `
            <h3>${task.title} <span style="font-size:12px; color:#555;">(${task.status})</span></h3>
            <p>Difficulty: ${task.difficulty}</p>
            <p>Progress: ${task.progress_percentage}%</p>
            <button onclick="deleteGoal(${task.task_id})">Delete Goal</button>
            <div id="subtasks-${task.task_id}">Loading subtasks...</div>
        `;

        container.appendChild(goalDiv);
        loadSubtasks(task.task_id);
    });
}



// LOAD SUBTASKS
async function loadSubtasks(task_id) 
{
    const container = document.getElementById(`subtasks-${task_id}`);
    const res = await fetch(`http://127.0.0.1:5000/tasks/${task_id}/subtasks`);
    const data = await res.json();

    if (!data.subtasks || data.subtasks.length === 0) 
    {
        container.innerHTML = "<p>No subtasks yet.</p>";
        return;
    }

    container.innerHTML = "";
    data.subtasks.forEach(sub => 
    {
        const subDiv = document.createElement("div");
        subDiv.className = "subtask";
        subDiv.innerHTML = `
            <input type="checkbox" id="sub-${sub.subtask_id}" ${sub.status === "completed" ? "checked" : ""} onchange="toggleSubtask(${sub.subtask_id})">
            <label for="sub-${sub.subtask_id}">${sub.title}</label>
        `;
        container.appendChild(subDiv);
    });
}



// TOGGLE SUBTASK STATUS
async function toggleSubtask(subtask_id) 
{
    const checkbox = document.getElementById(`sub-${subtask_id}`);
    const status = checkbox.checked ? "completed" : "pending";

    const res = await fetch(`http://127.0.0.1:5000/subtask/${subtask_id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status })
    });

    const data = await res.json();
    if (res.status === 200) loadGoals();
    else alert(data.error || "Failed to update subtask");
}



// DELETE GOAL
async function deleteGoal(task_id) 
{
    if (!confirm("Are you sure you want to delete this goal?")) return;

    const res = await fetch(`http://127.0.0.1:5000/task/${task_id}`, {
        method: "DELETE"
    });

    const data = await res.json();
    if (res.status === 200) loadGoals();
    else alert(data.error || "Failed to delete goal");
}



// INITIAL LOAD
loadGoals();
