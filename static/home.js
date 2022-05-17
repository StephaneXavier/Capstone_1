const $sub = $('#submit')
const $busNo = $('#busNo')
const $stopNo = $('#stopNo')
const $response = $('#response')
const $to_date = $('#to_date')
const $from_date = $('#from_date')

let counter = 1

function display_db_query_result(db_resp) {
    const c = counter
    counter += 1
    return `
    <div class='col-3'>
    <div class="card" style="width: 18rem;">
    <div class="card-body">

      <h5 class="card-title">
      Delay:${db_resp.data.delay}, no shows: ${db_resp.data.noShow}</h5>
     
     
      <p class="card-text"> Search parameters<br/>
      bus # - ${db_resp.search_param.busNo}</br>
      stop # - ${db_resp.search_param.stopNo}</br>
      from - ${db_resp.search_param.from_date} </br>
      to - ${db_resp.search_param.to_date}</p>
      
    </div>
    </div>
  </div>`

}


$('#clear').on('click', (e) => {
    e.preventDefault()
    $response.empty()
    counter = 0
})


function form_data() {
    return {
        busNo: $busNo.val(),
        stopNo: $stopNo.val(),
        to_date: $to_date.val() || '',
        from_date: $from_date.val() || '',
    }
}

$sub.on('click', async (e) => {
    e.preventDefault()
    // $response.text('')
    params = form_data()

    t = await axios.get('/db_request', { params: params })
    $response.append(display_db_query_result(t.data))

})


