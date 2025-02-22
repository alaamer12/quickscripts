import os.path
from datetime import datetime


def generate_profile_card():
    # Collect user input
    name = input("Enter The name: ").title()
    role = input("Enter The role: ").title()
    degree = input("Enter Role expertise: ").title()
    image_url = ""

    constraints = input("Enter The constraints (comma-separated): ").split(',')
    additional = input("Enter additional information (comma-separated): ").split(',')

    contact = input("Enter Phone number or contact info: ")
    availability = input("Enter The availability: ")
    last_updated = input("Enter last updated date (YYYY-MM-DD) or leave blank for today: ")
    if not last_updated.strip():
        last_updated = datetime.now().strftime("%Y-%m-%d")

    # Prepare the specialties and constraints for HTML
    specialty_list = ''.join(f'<li>{item.strip()}</li>' for item in additional if item.strip())
    constraints_list = ''.join(f'<li>{item.strip()}</li>' for item in constraints if item.strip())

    # Create the HTML content
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} Card</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }}
        .profile-card {{
            border: 1px solid #ccc;
            border-radius: 8px;
            padding: 16px;
            max-width: 90%;
            width: 300px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            background-color: white;
            position: relative;
            overflow: hidden;
        }}
        .wallpaper {{
            height: 100px;
            border-radius: 8px 8px 0 0;
            position: relative;
            overflow: hidden;
        }}
        .profile-card img,
        .default-avatar {{
            width: 100px;
            height: 100px;
            border-radius: 50%;
            position: absolute;
            top: 60px;
            left: 50%;
            transform: translateX(-50%);
            border: 3px solid white;
            display: none; /* Initially hide image */
        }}
        .default-avatar {{
            display: block; /* Show default avatar */
        }}
        .profile-details {{
            margin-top: 80px;
        }}
        .profile-details h2 {{
            margin: 10px 0 5px;
            word-wrap: break-word;
        }}
        .profile-details p {{
            margin: 5px 0;
            word-wrap: break-word;
        }}
        .profile-attributes {{
            display: flex;
            flex-direction: column;
            margin-top: 10px;
            position: relative;
        }}
        .profile-attributes div {{
            width: 100%;
            text-align: left;
            margin-bottom: 10px;
        }}
        .profile-attributes h4 {{
            margin: 5px 0;
            color: #333;
        }}
        .profile-attributes ul {{
            list-style-type: none;
            padding: 0;
            margin: 0;
        }}
        .profile-attributes li {{
            margin: 3px 0;
            padding: 5px;
            background: #f0f0f0;
            border-radius: 4px;
        }}
        .horizontal-line {{
            border-top: 2px solid #ccc;
            margin: 15px 0;
        }}
        .metadata {{
            margin-top: 10px;
            font-size: 0.9em;
            color: #666;
        }}
        @media (max-width: 400px) {{
            .profile-card {{
                max-width: 95%;
            }}
        }}
    </style>
</head>
<body>

<div class="profile-card" id="profileCard">
    <div class="wallpaper" id="wallpaper"></div>
    <img src="{image_url}" alt="Profile Picture" id="profileImage">
    <div class="default-avatar" id="defaultAvatar"></div>
    <div class="profile-details">
        <h2 id="profileName">{name}</h2>
        <p id="profileRole">Role: {role}</p>
        <p id="profileDegree">Degree of Expertise: {degree}</p>
    </div>
    <div class="profile-attributes">
        <div>
            <h4>Constraints:</h4>
            <ul id="profileConstraints">{constraints_list}</ul>
        </div>
        <div>
            <h4>Additional:</h4>
            <ul id="profileAdditional">{specialty_list}</ul>
        </div>
    </div>
    <div class="horizontal-line"></div>
    <p id="profileContact">Contact: {contact}</p>
    <p id="profileAvailability">Availability: {availability}</p>
    <div class="metadata">
        <p>Last updated: <span id="profileLastUpdated">{last_updated}</span></p>
    </div>
</div>

<button id="downloadBtn">Download Profile Card as Image</button>

<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
<script>
    function generateRandomColor() {{
        const letters = '0123456789ABCDEF';
        let color = '#';
        for (let i = 0; i < 6; i++) {{
            color += letters[Math.floor(Math.random() * 16)];
        }}
        return color;
    }}

    function createDefaultAvatar(initial) {{
        const avatarDiv = document.getElementById('defaultAvatar');
        avatarDiv.style.backgroundColor = generateRandomColor();
        avatarDiv.style.width = '100px';
        avatarDiv.style.height = '100px';
        avatarDiv.style.borderRadius = '50%';
        avatarDiv.style.color = 'white';
        avatarDiv.style.display = 'flex';
        avatarDiv.style.alignItems = 'center';
        avatarDiv.style.justifyContent = 'center';
        avatarDiv.style.fontSize = '40px';
        avatarDiv.innerText = initial;
    }}

    function setProfileData(image, name, age, role, degree, additional, constraints, contact, availability, lastUpdated) {{
        const profileImage = document.getElementById('profileImage');
        const defaultAvatar = document.getElementById('defaultAvatar');
        const wallpaper = document.getElementById('wallpaper');

        const initial = name ? name.charAt(0).toUpperCase() : '';
        const avatarBgColor = generateRandomColor();

        if (image) {{
            profileImage.src = image;
            profileImage.alt = `${{name}}'s Profile Picture`;
            profileImage.onload = function() {{
                defaultAvatar.style.display = 'none';
                profileImage.style.display = 'block';
            }};
            profileImage.style.display = 'block'; // Show the profile image if set
            defaultAvatar.style.display = 'none'; // Hide the default avatar
            wallpaper.style.backgroundColor = adjustColorBrightness(avatarBgColor, -50); // Adjust wallpaper color for contrast
        }} else {{
            createDefaultAvatar(initial);
            profileImage.style.display = 'none'; // Hide the profile image
            wallpaper.style.backgroundColor = avatarBgColor; // Use avatar background color
        }}

        document.getElementById('profileName').innerText = name || 'N/A';
        document.getElementById('profileAge').innerText = 'Age: ' + (age || 'N/A');
        document.getElementById('profileRole').innerText = 'Role: ' + (role || 'N/A');
        document.getElementById('profileDegree').innerText = 'Degree of Expertise: ' + (degree || 'N/A');

        const specialtyList = document.getElementById('profileAdditional');
        specialtyList.innerHTML = '';
        (additional || []).forEach(item => {{
            const li = document.createElement('li');
            li.innerText = item || 'N/A';
            specialtyList.appendChild(li);
        }});

        const constraintsList = document.getElementById('profileConstraints');
        constraintsList.innerHTML = '';
        (constraints || []).forEach(item => {{
            const li = document.createElement('li');
            li.innerText = item || 'N/A';
            constraintsList.appendChild(li);
        }});

        document.getElementById('profileContact').innerText = 'Contact: ' + (contact || 'N/A');
        document.getElementById('profileAvailability').innerText = 'Availability: ' + (availability || 'N/A');
        document.getElementById('profileLastUpdated').innerText = lastUpdated || 'N/A';
    }}

    function adjustColorBrightness(hex, percent) {{
        const num = parseInt(hex.slice(1), 16);
        const amt = Math.floor(2.55 * percent);
        const r = (num >> 16) + amt;
        const g = (num >> 8 & 0x00FF) + amt;
        const b = (num & 0x0000FF) + amt;
        return "#" + (0x1000000 + (r < 255 ? (r < 1 ? 0 : r) : 255) * 0x10000 + (g < 255 ? (g < 1 ? 0 : g) : 255) * 0x100 + (b < 255 ? (b < 1 ? 0 : b) : 255)).toString(16).slice(1);
    }}

    document.getElementById('downloadBtn').addEventListener('click', function() {{
        html2canvas(document.querySelector("#profileCard")).then(canvas => {{
            const link = document.createElement('a');
            link.download = 'profile_card.png';
            link.href = canvas.toDataURL();
            link.click();
        }});
    }});

    setProfileData("{image_url}", "{name}", "{role}", "{degree}", [{', '.join(f'"{item.strip()}"' for item in additional if item.strip())}], [{', '.join(f'"{item.strip()}"' for item in constraints if item.strip())}], "{contact}", "{availability}", "{last_updated}");
</script>

</body>
</html>
"""
    DIR = r"inventory"

    file_name = name.replace(" ", "_")
    if not file_name.endswith(".html"):
        file_name += ".html"
    file_path = os.path.join(DIR, file_name)
    if os.path.exists(file_path):
        import random
        file_path = os.path.join(DIR, f"{file_name[:-5]}_{random.randint(10, 99)}.html")

    # Save to an HTML file
    with open(file_path, "w") as file:
        file.write(html_content)

    print("Profile card generated: profile_card.html")


if __name__ == "__main__":
    generate_profile_card()
