function fillFilmList() {
    fetch('/lab7/rest-api/films/')
    .then(function (data) {
        return data.json();
    })
    .then(function (films) {
        let tbody = document.getElementById('film-list');
        tbody.innerHTML = '';
        
        // Если нет фильмов
        if (films.length === 0) {
            let tr = document.createElement('tr');
            let td = document.createElement('td');
            td.colSpan = 4;
            td.innerText = 'Нет фильмов';
            td.style.textAlign = 'center';
            tr.append(td);
            tbody.append(tr);
            return;
        }
        
        for(let i = 0; i < films.length; i++) {
            let film = films[i];
            let tr = document.createElement('tr');
            
            let tdTitleRus = document.createElement('td');
            let tdTitle = document.createElement('td');
            let tdYear = document.createElement('td');
            let tdActions = document.createElement('td');

            tdTitleRus.innerText = film.title_ru || '';
            tdTitle.innerHTML = film.title ? '<i>' + film.title + '</i>' : '';
            tdYear.innerText = film.year || '';
            
            // Исправлено: передаем film.id вместо i
            let editButton = document.createElement('button');
            editButton.innerText = 'редактировать';
            editButton.onclick = function() {
                editFilm(film.id);
            }

            let delButton = document.createElement('button');
            delButton.innerText = 'удалить';
            delButton.onclick = function() {
                deleteFilm(film.id, film.title_ru || 'без названия');
            }

            tdActions.append(editButton);
            tdActions.append(delButton);
            
            tr.append(tdTitleRus);
            tr.append(tdTitle);
            tr.append(tdYear);
            tr.append(tdActions);

            tbody.append(tr);
        }
    })
    .catch(function(err) {
        console.error('Ошибка при загрузке фильмов:', err);
        let tbody = document.getElementById('film-list');
        tbody.innerHTML = '';
        let tr = document.createElement('tr');
        let td = document.createElement('td');
        td.colSpan = 4;
        td.innerText = 'Ошибка загрузки фильмов';
        td.style.textAlign = 'center';
        td.style.color = 'red';
        tr.append(td);
        tbody.append(tr);
    });
}

function deleteFilm(id, title) {
    if(! confirm(`Вы точно хотите удалить фильм "${title}"?`))
        return;
    
    fetch(`/lab7/rest-api/films/${id}`, {method: 'DELETE'})
        .then(function(response) {
            if (response.status === 204) {
                fillFilmList();
            } else {
                console.error('Ошибка удаления:', response.status);
                alert('Ошибка при удалении фильма');
            }
        })
        .catch(function(error) {
            console.error('Ошибка сети:', error);
            alert('Ошибка сети при удалении');
        });
}

function showModal() {
    document.getElementById('description-error').innerText = '';
    document.getElementById('title-error').innerText = '';
    document.getElementById('title-ru-error').innerText = '';
    document.getElementById('year-error').innerText = '';
    document.querySelector('div.modal').style.display = 'block';
}

function hideModal() {
    document.querySelector('div.modal').style.display = 'none';
}

function cancel() {
    hideModal();
}

function addFilm() {
    document.getElementById('id').value = '';
    document.getElementById('title').value = '';
    document.getElementById('title-ru').value = '';
    document.getElementById('year').value = '';
    document.getElementById('description').value = '';
    showModal();
}

function sendFilm() {
    const id = document.getElementById('id').value;
    const film = {
        title: document.getElementById('title').value.trim(),
        title_ru: document.getElementById('title-ru').value.trim(),
        year: document.getElementById('year').value.trim(),
        description: document.getElementById('description').value.trim()
    }

    // Исправлено: URL для POST запроса
    const url = id === '' ? '/lab7/rest-api/films/' : `/lab7/rest-api/films/${id}`;
    const method = id === '' ? 'POST' : 'PUT';
    
    // Очистка ошибок
    document.getElementById('description-error').innerText = '';
    document.getElementById('title-error').innerText = '';
    document.getElementById('title-ru-error').innerText = '';
    document.getElementById('year-error').innerText = '';

    fetch(url, {
        method: method,
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(film)
    })
    .then(function(resp) {
        if(resp.ok) {
            fillFilmList();
            hideModal();
            return {};
        }
        return resp.json();
    })
    .then(function(errors) {
        if (!errors) return;
        
        if (errors.description)
            document.getElementById('description-error').innerText = errors.description;
        if (errors.title)
            document.getElementById('title-error').innerText = errors.title;
        if (errors.title_ru)
            document.getElementById('title-ru-error').innerText = errors.title_ru;
        if (errors.year)
            document.getElementById('year-error').innerText = errors.year;
        if (errors.error)
            document.getElementById('description-error').innerText = errors.error;
    })
    .catch(function(err) {
        console.error('Ошибка при отправке:', err);
        document.getElementById('description-error').innerText = 'Ошибка сети';
    });
}

function editFilm(id) {
    fetch(`/lab7/rest-api/films/${id}`)
    .then(function (data) {
        if (!data.ok) {
            throw new Error('Фильм не найден');
        }
        return data.json();
    })
    .then(function (film) {
        document.getElementById('id').value = id;
        document.getElementById('title').value = film.title || '';
        document.getElementById('title-ru').value = film.title_ru || '';
        document.getElementById('year').value = film.year || '';
        document.getElementById('description').value = film.description || '';
        showModal();
    })
    .catch(function(error) {
        console.error('Ошибка при загрузке фильма:', error);
        alert('Ошибка при загрузке фильма для редактирования');
    });
}