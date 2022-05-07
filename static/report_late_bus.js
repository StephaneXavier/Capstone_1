const $delay = $('#delay')
const $noShow = $('#no_show')


$noShow.on('click', () => {
    $delay.val('')
})

$('button').on('click', (e) => {
    if ($noShow.is(':checked') && $delay.val()) {
        e.preventDefault()
        alert('Choose bus delay or no show, not both')
    }
    if (!$noShow.is(':checked') && $delay.val() == '') {
        e.preventDefault()
        alert('Fill in bus delay or click no show')
    }
    if (int($delay.val()) <= 0) {
        e.preventDefault()
        alert('Bus delay cannot be 0 or less')
    }

})