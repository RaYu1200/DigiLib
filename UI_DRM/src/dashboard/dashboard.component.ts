import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'drm-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent {

  constructor(private _roter : Router){}
  upload(){
    this._roter.navigate(['upload']);
  }

  search(){
    this._roter.navigate(['search']);


  }
}
