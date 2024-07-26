import { Component } from '@angular/core';
import { DashaboarService, IItems } from '../Service/dashboard.service';
import { HttpParams } from '@angular/common/http';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'drm-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.scss']
})
export class SearchComponent {
  value:string ='';


  data: IItems[];
  constructor(private _httpService : DashaboarService, private _snackBar: MatSnackBar){


  }


  onSearch(){
    let Params  = {};
    Params['searchText'] = this.value;
    Params['sortBy'] = "Date";

    console.log("ankur")
    this._httpService.getRecords(Params).subscribe((data)=>{

      this.data = data.metaData.Items;

      if(this.data.length==0){
        const ref =   this._snackBar.open('No Reasults Found');
      setTimeout(()=>{
        ref.dismiss();
      },2000);
      }

    });
  }
} 
