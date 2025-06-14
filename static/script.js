// ✅ script.js المعدل لفتح صفحة مستقلة عند الضغط على Edit وإزالة المودال بالكامل

$(document).ready(function () {
    let debounceTimer;

    $('#searchInput').on('input', function () {
        clearTimeout(debounceTimer);
        let query = $(this).val().trim();

        if (query === "") {
            $('#assetResults .table-container').empty();
            $('#pmResults .table-container').empty();
            return;
        }

        debounceTimer = setTimeout(() => {
            $.ajax({
                url: '/search',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ query }),
                success: function (data) {
                    if (data.error) {
                        alert("Search Error: " + data.error);
                        return;
                    }

                    // بناء نتائج الـ Assets مع زر تعديل
                    let assetHTML = '';
                    if (Array.isArray(data.assets) && data.assets.length > 0) {
                        data.assets.forEach((item, index) => {
                            assetHTML += `
                                <div class="sheet-title">
                                    <h6>Sheet: ${escapeHtml(item.SheetName)}, Row: ${item.RowIndex + 2}</h6>
                                </div>
                                <table class="table table-bordered table-sm table-striped" id="assetTable${index}">
                                    <tbody>`;
                            for (let key in item.data) {
                                assetHTML += `<tr><td><strong>${escapeHtml(key)}</strong></td><td>${escapeHtml(item.data[key])}</td></tr>`;
                            }
                            assetHTML += `</tbody></table>
                                <a class="btn btn-primary btn-sm"
                                   href="/edit?type=Asset&sheet=${escapeHtmlAttr(item.SheetName)}&row=${item.RowIndex}">
                                    Edit
                                </a>
                                <hr/>`;
                        });
                    } else {
                        assetHTML = '<div class="alert alert-warning">No results found in Asset List.</div>';
                    }
                    $('#assetResults .table-container').html(assetHTML);

                    // بناء نتائج الـ PM مع زر تعديل
                    let pmHTML = '';
                    if (Array.isArray(data.pm) && data.pm.length > 0) {
                        data.pm.forEach((item, index) => {
                            pmHTML += `
                                <div class="sheet-title">
                                    <h6>Sheet: ${escapeHtml(item.SheetName)}, Row: ${item.RowIndex + 2}</h6>
                                </div>
                                <table class="table table-bordered table-sm table-striped" id="pmTable${index}">
                                    <tbody>`;
                            for (let key in item.data) {
                                pmHTML += `<tr><td><strong>${escapeHtml(key)}</strong></td><td>${escapeHtml(item.data[key])}</td></tr>`;
                            }
                            pmHTML += `</tbody></table>
                                <a class="btn btn-primary btn-sm"
                                   href="/edit?type=PM&sheet=${escapeHtmlAttr(item.SheetName)}&row=${item.RowIndex}">
                                    Edit
                                </a>
                                <hr/>`;
                        });
                    } else {
                        pmHTML = '<div class="alert alert-warning">No results found in PM List.</div>';
                    }
                    $('#pmResults .table-container').html(pmHTML);
                },
                error: function () {
                    alert("An error occurred while searching.");
                }
            });
        }, 300);
    });

    // دوال مساعدة
    function escapeHtml(text) {
        if (typeof text !== 'string') return text;
        return text.replace(/[&<>"']/g, function (m) {
            switch (m) {
                case '&': return '&amp;';
                case '<': return '&lt;';
                case '>': return '&gt;';
                case '"': return '&quot;';
                case "'": return '&#39;';
                default: return m;
            }
        });
    }

    function escapeHtmlAttr(text) {
        if (typeof text !== 'string') return text;
        return text.replace(/['"]/g, function (m) {
            return m === '"' ? '&quot;' : '&#39;';
        });
    }
});
