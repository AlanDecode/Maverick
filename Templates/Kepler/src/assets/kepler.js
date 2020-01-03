/* eslint-disable no-console */
/* eslint-disable no-undef */
console.log(' %c Maverick & Kepler By AlanDecode %c https://www.imalan.cn/ ', 'color: #fadfa3; background: #23b7e5; padding:5px;', 'padding:5px;');

var initPage = function (refresh) {
    $('.toggle_sidebar').click(function () {
        $(this).parent().parent().toggleClass('open');
    });
    $('.go-external').click(function() {
        window.open($(this).siblings('a').attr('href'), '_blank');
    });

    var toc_sel = '#content article';
    if ($(toc_sel).length && $('#toc').length) {
        $.each($(toc_sel).find('h1, h2, h3, h4, h5, h6'), function (i, item) {
            $(item).attr('id', 'toc_' + String(i + 1));
        });

        if (refresh) {
            tocbot.refresh({
                // Where to render the table of contents.
                tocSelector: '#toc',
                // Where to grab the headings to build the table of contents.
                contentSelector: '#content article',
                // Which headings to grab inside of the contentSelector element.
                headingSelector: 'h1, h2, h3, h4, h5, h6',
                // For headings inside relative or absolute positioned containers within content.
                hasInnerContainers: true,
                collapseDepth: 7
            });
        } else {
            tocbot.init({
                // Where to render the table of contents.
                tocSelector: '#toc',
                // Where to grab the headings to build the table of contents.
                contentSelector: '#content article',
                // Which headings to grab inside of the contentSelector element.
                headingSelector: 'h1, h2, h3, h4, h5, h6',
                // For headings inside relative or absolute positioned containers within content.
                hasInnerContainers: true,
                collapseDepth: 7
            });
        }
    }

    $('#content-wrapper').click(function () {
        $('body').removeClass('toc-open').removeClass('navbar-open');
    });

    (function () {
        var domain = document.domain;
        var els = document.getElementsByTagName('a');
        for (var index = 0; index < els.length; index++) {
            var element = els[index];
            var target = element.getAttribute('target');
            if (typeof target === 'undefined' || (target != '' && target != '_self')) {
                if (element.host != domain) {
                    element.setAttribute('target', '_blank');
                }
            }
        }
    })();

    (function () {
        var tuneBilibili = function () {
            var iframes = document.getElementsByTagName('iframe');

            for (var index = 0; index < iframes.length; index++) {
                var iframe = iframes[index];
                var src = iframe.src;

                if (typeof src === 'string' && src.indexOf('player.bilibili.com') > -1) {
                    iframe.classList.add('bili-player');

                    if (src.indexOf('&high_quality') < 0) {
                        src += '&high_quality=1'; // enable high quality
                        iframe.setAttribute('src', src);
                    }

                    // by default 9:16
                    var height = iframe.clientWidth * 0.5625;

                    // is aspect ratio is explicitly specified
                    if (iframe.getAttribute('data-ratio') != undefined)
                        height = parseFloat(iframe.getAttribute('data-ratio')) * iframe.clientWidth;

                    // show control panel with screen wider than 540
                    if (window.innerWidth >= 540)
                        height += 120;

                    iframe.style.height = height + 'px';
                }
            }
        };

        tuneBilibili();
        window.addEventListener('resize', tuneBilibili);
    })();

    (function () {
        var domain = document.domain;
        $.each($('a:not(a[target="_blank"], a[no-pjax])'), function (i, item) {
            if (item.host == domain) {
                $(item).addClass('pjax');
            }
        });
        $(document).pjax('a.pjax', {
            container: '#pjax-container',
            fragment: '#pjax-container',
            timeout: 8000
        });
    })();

    if (refresh) {
        renderMathInElement(document.body, mathOpts);
        if (typeof initValine == 'function') {
            initValine();
        }
    }
};

(function () {
    $(document).ready(function () {
        initPage(false);
    });

    $(document).on('pjax:send', function () {
        $('body').removeClass('navbar-open').removeClass('toc-open');
        NProgress.configure({ showSpinner: false });
        NProgress.start();
    });

    $(document).on('pjax:complete', function () {
        NProgress.done();
        initPage(true);
    });
})();
