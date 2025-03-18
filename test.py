
def get_challenges(body_id):
        container = soup.find('div', id=body_id, class_="collapse")
        if not container:
            return []

        challenges = []
        for challenge in container.find_all('div', class_='challenge-row'):
            try:
                title_tag = challenge.find('h4')
                time_tag = challenge.find('h6')
                
                full_title = title_tag.get_text(strip=True)
                clean_name = re.sub(r'($ easy $|$ hard $|\uf024\s*|\d+ pts?)', '', full_title).strip()
                level = ''.join(re.findall(r'\d+', full_title)) or '0'

                #timestamp = None
                parts = time_tag.get_text(strip=True).split(':', 1)
                timestamp = parts[1].strip()

                challenges.append({
                    'name': clean_name,
                    'level': level,
                    'timestamp': timestamp
                })
            except Exception as e:
                continue
        
        return challenges