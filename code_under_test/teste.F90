subroutine tst_1(A1,x)
   !! ## brief
   !!
   !! Author: autor
   !!
   !! E-mail: <mailto:email>
   !!
   !! Date: 14Fevereiro2023 17:32
   !!
   !! #####Version: version
   !!
   !! ---
   !! **Full description**:
   !!
   !! brief
   !!
   !! ** History**:
   !!
   !! --- 
   !! ** Licence **: Under the terms of the GNU General Public version 3
   !!   <img src="https://www.gnu.org/graphics/gplv3-127x51.png width="63">
   !!--------------------------------------------------------------------------------------------
!teste para tamanho de linha -------------------------------------------------------------------------------------------------------
   USE mpi;USE modCobvParGF !!------------------------------------------------------------------------------------------------------

   implicit none ; character(len=*), parameter :: p_procedure_name = 'tst' 
   !Parameters:
   
   !!
   
   !subroutine name

   !Variables (input, output, inout)
   real, intent(inout) :: A1(:)
   integer, intent(in) :: x
   integer initiate_declaration=10
   
   !Local variables:
   integer :: i, ift

   !Code:

   open(unit=23, file="teste.txt",status="new",action="write");  write(23,*) "teste"

   do i=1,x
      A1(i)= A1(i) * 2.0
      do j=1,x
         A2(j)= A1(j) * 2.0
      enddo   
   enddo

   IF(x==30) then
      A1(30) = 145.7
   else 
      goto 30
   endif 

   if(x==45) then
      A1(15) = 145.0
   endif
   
30 continue
   if(x>6) then
      ift = 7
      write(unit=23,*) ift
   ELSE
      ift = 8
   end if

   select case (x)
   case(1)
      print *, "1"
   case(2)
      print *, "2"
   case default
      print *, 'nao sei'
   end select

   if(x<1) write(unit=23,*) ift

   close(unit=23)

end subroutine tst_1


subroutine ifx(  b_teste &
              ,c_teste)
   !! ## teste
   !!
   !! Author: autor
   !!
   !! E-mail: <mailto:email>
   !!
   !! Date: 15Fevereiro2023 09:04
   !!
   !! #####Version: version
   !!
   !! ---
   !! **Full description**:
   !!
   !! teste
   !!
   !! ** History**:
   !!
   !! --- 
   !! ** Licence **: Under the terms of the GNU General Public version 3
   !!   <img src="https://www.gnu.org/graphics/gplv3-127x51.png width="63">
   !!

   IMPLICIT NONE
   !Parameters: 
   character(len=*), parameter :: procedureName = 'xxx'
   !! subroutine name ------->>>>>>inicio dos erros nas linhas -> 105
   
   real,  parameter :: g = 9.8 

   !! constante geométrica pi

   !Variables (input, output, inout)
   real, intent(in) :: b_teste, c_Teste

   !Local variables: 
   real :: a_Teste = 23
   integer, allocatable :: x_alloc(:) !teste xml ->> 115
   integer, allocatable :: y_alloc(:)
   character(len=20) :: nome

   character(len=20) :: name_lw, NAME_UPPER, Name_first_upper
   !namelist /TESTE/ name_lw, NAME_UPPER, Name_first_upper

   !Code:  ->> 121
   name_lw = "lower name"
   !NAME_UPPER = "KLCLAUDIO"
   !Name_first_upper = "Klclaudio"
   !write(6,TESTE)

   a_Teste = 3.45 

   b_Teste = 3.45 + &
             3.50

   c_Teste = 5.0 &
           + 7.0        

   a_teste= b_teste
   nome = "Luiz"
   
   
   if (.not.allocated(x_alloc)) allocate(x_alloc)
   
   if (.not.allocated(y_alloc)) allocate(y_alloc)
   
!   if (allocated(y_alloc)) deallocate(y_alloc)

   if (allocated(x_alloc)) deallocate(x_alloc)

   
end subroutine ifx

module test
   
end module
