import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AddFileComponent } from './add-file/add-file.component';
import { SharedModule } from 'src/shared/shared.module';
import { DashboardComponent } from './dashboard.component';
import { RouterModule } from '@angular/router';
import { DashboardRoutingModule } from './dashboard.roting.module';
import { AngularMaterialsModule } from 'src/shared/material.module';
import { SearchComponent } from './search/search.component';
import { FormsModule, ReactiveFormsModule  } from '@angular/forms';
import { HttpClient } from '@angular/common/http';


@NgModule({
  declarations: [
    AddFileComponent,
    DashboardComponent,
    SearchComponent
  ],
  imports: [
    CommonModule,
    SharedModule,
    RouterModule,
    DashboardRoutingModule,
    AngularMaterialsModule,
    FormsModule,
    ReactiveFormsModule
  ],
  providers:[HttpClient]
})
export class DashboardModule { }
