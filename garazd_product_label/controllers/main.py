# Copyright © 2023 Garazd Creation (<https://garazd.biz>)
# @author: Yurii Razumovskyi (<support@garazd.biz>)
# @author: Iryna Razumovska (<support@garazd.biz>)
# License OPL-1 (https://www.odoo.com/documentation/15.0/legal/licenses.html).

from odoo import http
from odoo.http import request

from ..wizard.print_product_label import LABEL_ATTACHMENT_NAME


class PrintPDF(http.Controller):

    @http.route(
        '/print_label/<string:attachment_id>',
        type='http',
        auth='user',
        sitemap=False,
    )
    def print_label_pdf(self, attachment_id=None, **kwargs):
        if not attachment_id:
            return request.not_found()

        try:
            attachment_id = int(attachment_id)
        except ValueError:
            return request.not_found()

        attachment = request.env['ir.attachment'].sudo().search([
            ('name', '=', LABEL_ATTACHMENT_NAME),
            ('mimetype', '=', 'application/pdf'),
            ('id', '=', attachment_id),
        ])

        if not attachment:
            return request.not_found()

        pdf_url = f'/web/content/{attachment_id}'
        return request.render(
            'garazd_product_label.print_product_label_pdf_template',
            {'title': 'Print Product Labels', 'pdf_url': pdf_url},
        )

    @http.route(
        '/print_label_preview/<int:wizard_id>',
        type='http',
        auth='user',
        sitemap=False,
    )
    def print_label_preview(self, wizard_id=None, **kwargs):
        if not wizard_id:
            return request.not_found()
        wizard = request.env['print.product.label'].sudo().browse(wizard_id)
        if not wizard.exists():
            return request.not_found()
        report = wizard._prepare_report()
        labels = wizard.get_labels_to_print()
        html_bytes, _ = report.with_context(print_mode='html')._render_qweb_html(report.report_name, labels.ids)
        html_content = html_bytes.decode('utf-8') if isinstance(html_bytes, bytes) else html_bytes

        wrapped_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8"/>
    <title>Product Label Preview (50x25 mm)</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            background: #2b2b36;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            color: #ffffff;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
        }}
        .preview-header {{
            width: 100%;
            background: #1e1e2d;
            padding: 12px 24px;
            box-sizing: border-box;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.3);
            position: sticky;
            top: 0;
            z-index: 100;
        }}
        .preview-title {{
            font-size: 16px;
            font-weight: 600;
            color: #ffffff;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .badge-dim {{
            background: #7239ea;
            color: #fff;
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 12px;
        }}
        .btn-print {{
            background: #009ef7;
            color: #ffffff;
            border: none;
            padding: 8px 16px;
            border-radius: 6px;
            font-weight: 600;
            cursor: pointer;
            text-decoration: none;
        }}
        .btn-print:hover {{
            background: #0086d1;
        }}
        .preview-body {{
            padding: 30px;
            display: flex;
            justify-content: center;
        }}
        .label-sheet-container {{
            background: #ffffff;
            color: #000000;
            padding: 10px;
            border-radius: 8px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.4);
            min-width: 100mm;
        }}
    </style>
</head>
<body>
    <div class="preview-header">
        <div class="preview-title">
            <span>Product Label Live Preview</span>
            <span class="badge-dim">50x25 mm (2 Columns)</span>
        </div>
        <button class="btn-print" onclick="window.print()">Print Page</button>
    </div>
    <div class="preview-body">
        <div class="label-sheet-container">
            {html_content}
        </div>
    </div>
</body>
</html>"""
        return request.make_response(wrapped_html, headers=[('Content-Type', 'text/html; charset=utf-8')])
